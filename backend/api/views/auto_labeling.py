import json

import botocore.exceptions
import requests
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.menu import Options
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.pipeline import pipeline
from auto_labeling_pipeline.postprocessing import PostProcessor
from auto_labeling_pipeline.task import TaskFactory
from django.shortcuts import get_object_or_404
from django_drf_filepond.models import TemporaryUpload
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions import (AutoLabelingException, AutoLabelingPermissionDenied,
                          AWSTokenError, SampleDataException,
                          TemplateMappingError, URLConnectionError)
from ..models import AutoLabelingConfig, Example, Project
from ..permissions import IsInProjectOrAdmin, IsProjectAdmin
from ..serializers import (AutoLabelingConfigSerializer,
                           get_annotation_serializer)


class AutoLabelingTemplateListAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        options = Options.filter_by_task(task_name=project.project_type)
        option_names = [o.name for o in options]
        return Response(option_names, status=status.HTTP_200_OK)


class AutoLabelingTemplateDetailAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        option_name = self.kwargs['option_name']
        option = Options.find(option_name=option_name)
        return Response(option.to_dict(), status=status.HTTP_200_OK)


class AutoLabelingConfigList(generics.ListCreateAPIView):
    serializer_class = AutoLabelingConfigSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.auto_labeling_config

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)


class AutoLabelingConfigDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AutoLabelingConfig.objects.all()
    serializer_class = AutoLabelingConfigSerializer
    lookup_url_kwarg = 'config_id'
    permission_classes = [IsAuthenticated & IsProjectAdmin]


class AutoLabelingConfigTest(APIView):
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
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return execute_pipeline(
            text=test_input,
            project_type=project.project_type,
            model_name=serializer.data.get('model_name'),
            model_attrs=serializer.data.get('model_attrs'),
            template=serializer.data.get('template'),
            label_mapping=serializer.data.get('label_mapping')
        )


class AutoLabelingConfigParameterTest(APIView):
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
            response = model.send(example)
            return response
        except requests.exceptions.ConnectionError:
            raise URLConnectionError
        except botocore.exceptions.ClientError:
            raise AWSTokenError()
        except Exception as e:
            raise e

    def prepare_example(self):
        text = self.request.data['text']
        if self.project.is_task_of('text'):
            return text
        else:
            tu = TemporaryUpload.objects.get(upload_id=text)
            return tu.get_file_path()

    def post(self, *args, **kwargs):
        model = self.create_model()
        example = self.prepare_example()
        response = self.send_request(model=model, example=example)
        return Response(response, status=status.HTTP_200_OK)


class AutoLabelingTemplateTest(APIView):
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


class AutoLabelingMappingTest(APIView):
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


class AutoLabelingAnnotation(generics.CreateAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = get_annotation_serializer(task=project.project_type)
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()
        queryset = model.objects.filter(example=self.kwargs['example_id'])
        if not project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            raise AutoLabelingException()
        labels = self.extract()
        labels = self.transform(labels)
        serializer = self.get_serializer(data=labels, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_example(self, project):
        example = get_object_or_404(Example, pk=self.kwargs['example_id'])
        if project.is_task_of('text'):
            return example.text
        else:
            return str(example.filename)

    def extract(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        example = self.get_example(project)
        config = project.auto_labeling_config.first()
        if not config:
            raise AutoLabelingPermissionDenied()
        return execute_pipeline(
            text=example,
            project_type=project.project_type,
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


def execute_pipeline(text: str,
                     project_type: str,
                     model_name: str,
                     model_attrs: dict,
                     template: str,
                     label_mapping: dict):
    task = TaskFactory.create(project_type)
    model = RequestModelFactory.create(
        model_name=model_name,
        attributes=model_attrs
    )
    template = MappingTemplate(
        label_collection=task.label_collection,
        template=template
    )
    post_processor = PostProcessor(label_mapping)
    labels = pipeline(
        text=text,
        request_model=model,
        mapping_template=template,
        post_processing=post_processor
    )
    return labels.dict()
