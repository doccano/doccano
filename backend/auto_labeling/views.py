import abc
import json
from typing import List

import botocore.exceptions
import requests
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.menu import Options
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.postprocessing import PostProcessor
from auto_labeling_pipeline.task import TaskFactory
from django.shortcuts import get_object_or_404
from django_drf_filepond.models import TemporaryUpload
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Example, Project, Category, CategoryType, Annotation
from members.permissions import IsInProjectOrAdmin, IsProjectAdmin
from .pipeline.execution import execute_pipeline
from .exceptions import (AutoLabelingPermissionDenied,
                         AWSTokenError, SampleDataException,
                         TemplateMappingError, URLConnectionError)
from .models import AutoLabelingConfig
from .serializers import (AutoLabelingConfigSerializer, get_annotation_serializer)


class TemplateListAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request: Request, *args, **kwargs):
        task_name = request.query_params.get('task_name')
        options = Options.filter_by_task(task_name=task_name)
        option_names = [o.name for o in options]
        return Response(option_names, status=status.HTTP_200_OK)


class TemplateDetailAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        option = Options.find(option_name=self.kwargs['option_name'])
        return Response(option.to_dict(), status=status.HTTP_200_OK)


class ConfigList(generics.ListCreateAPIView):
    serializer_class = AutoLabelingConfigSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get_queryset(self):
        return AutoLabelingConfig.objects.filter(project=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_id'])


class ConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AutoLabelingConfig.objects.all()
    serializer_class = AutoLabelingConfigSerializer
    lookup_url_kwarg = 'config_id'
    permission_classes = [IsAuthenticated & IsProjectAdmin]


class FullPipelineTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        try:
            output = self.pass_config_validation()
            output = self.pass_pipeline_call(output)
            if not output:
                raise SampleDataException()
            return Response(
                data={'valid': True, 'labels': output},
                status=status.HTTP_200_OK
            )
        except requests.exceptions.ConnectionError:
            raise URLConnectionError()
        except botocore.exceptions.ClientError:
            raise AWSTokenError()
        except ValidationError as e:
            raise e
        except Exception as e:
            raise e

    def pass_config_validation(self):
        config = self.request.data['config']
        serializer = AutoLabelingConfigSerializer(data=config)
        serializer.is_valid(raise_exception=True)
        return serializer

    def pass_pipeline_call(self, serializer):
        test_input = self.request.data['input']
        return execute_pipeline(
            text=test_input,
            task_type=serializer.data.get('task_type'),
            model_name=serializer.data.get('model_name'),
            model_attrs=serializer.data.get('model_attrs'),
            template=serializer.data.get('template'),
            label_mapping=serializer.data.get('label_mapping')
        )


class RestAPIRequestTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def create_model(self):
        model_name = self.request.data['model_name']
        model_attrs = self.request.data['model_attrs']
        try:
            model = RequestModelFactory.create(model_name, model_attrs)
            return model
        except Exception:
            model = RequestModelFactory.find(model_name)
            schema = model.schema()
            required_fields = ', '.join(schema['required']) if 'required' in schema else ''
            raise ValidationError(
                'The attributes does not match the model.'
                'You need to correctly specify the required fields: {}'.format(required_fields)
            )

    def send_request(self, model, example):
        try:
            return model.send(example)
        except requests.exceptions.ConnectionError:
            raise URLConnectionError
        except botocore.exceptions.ClientError:
            raise AWSTokenError()
        except Exception as e:
            raise e

    def prepare_example(self):
        text = self.request.data['text']
        if self.project.is_text_project:
            return text
        else:
            tu = TemporaryUpload.objects.get(upload_id=text)
            return tu.get_file_path()

    def post(self, *args, **kwargs):
        model = self.create_model()
        example = self.prepare_example()
        response = self.send_request(model=model, example=example)
        return Response(response, status=status.HTTP_200_OK)


class LabelExtractorTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        response = self.request.data['response']
        template = self.request.data['template']
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        task = TaskFactory.create(project.project_type)
        template = MappingTemplate(
            label_collection=task.label_collection,
            template=template
        )
        try:
            labels = template.render(response)
        except json.decoder.JSONDecodeError:
            raise TemplateMappingError()
        if not labels.dict():
            raise SampleDataException()
        return Response(labels.dict(), status=status.HTTP_200_OK)


class LabelMapperTesting(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        response = self.request.data['response']
        label_mapping = self.request.data['label_mapping']
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        task = TaskFactory.create(project.project_type)
        labels = task.label_collection(response)
        post_processor = PostProcessor(label_mapping)
        labels = post_processor.transform(labels)
        return Response(labels.dict(), status=status.HTTP_200_OK)


class AutomatedDataLabeling(generics.CreateAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = get_annotation_serializer(task=project.project_type)
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        labels = self.extract()
        labels = self.transform(labels)
        serializer = self.get_serializer(data=labels, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def extract(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        example = get_object_or_404(Example, pk=self.kwargs['example_id'])
        config = project.auto_labeling_config.first()
        if not config:
            raise AutoLabelingPermissionDenied()
        return execute_pipeline(
            text=example.data,
            task_type=project.project_type,
            model_name=config.model_name,
            model_attrs=config.model_attrs,
            template=config.template,
            label_mapping=config.label_mapping
        )

    def transform(self, labels):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        for label in labels:
            label['example'] = self.kwargs['example_id']
            if 'label' in label:
                label['label'] = project.labels.get(text=label.pop('label')).id
        return labels


class AutomatedLabeling(abc.ABC, generics.CreateAPIView):
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None
    model = None
    task_type = None

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        example = get_object_or_404(Example, pk=self.kwargs['example_id'])
        configs = AutoLabelingConfig.objects.filter(task_type=self.task_type)
        for config in configs:
            labels = execute_pipeline(
                text=example.data,
                task_type=config.task_type,
                model_name=config.model_name,
                model_attrs=config.model_attrs,
                template=config.template,
                label_mapping=config.label_mapping
            )
            labels = self.transform(labels, example, project)
            labels = self.model.objects.filter_annotatable_labels(labels, project)
            self.model.objects.bulk_create(labels)
        return Response({'ok': True}, status=status.HTTP_201_CREATED)

    @abc.abstractmethod
    def transform(self, labels, example: Example, project: Project) -> List[Annotation]:
        raise NotImplementedError('Please implement this method in the subclass')


class AutomatedCategoryLabeling(AutomatedLabeling):
    model = Category
    task_type = 'Category'

    def transform(self, labels, example: Example, project: Project) -> List[Category]:
        mapping = {
            c.text: c for c in CategoryType.objects.filter(project=project)
        }
        categories = []
        for label in labels:
            if label['label'] not in mapping:
                continue
            label['example'] = example
            label['label'] = mapping[label['label']]
            label['user'] = self.request.user
            categories.append(Category(**label))
        return categories
