import collections
import json
import random

import botocore.exceptions
import requests
from auto_labeling_pipeline.menu import Options
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.task import TaskFactory
from auto_labeling_pipeline.postprocessing import PostProcessor
from auto_labeling_pipeline.pipeline import pipeline
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, F, Q
from libcloud.base import DriverType, get_driver
from libcloud.storage.types import ContainerDoesNotExistError, ObjectDoesNotExistError
from rest_framework import generics, filters, status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework_csv.renderers import CSVRenderer

from .exceptions import AutoLabelingException, AutoLabeliingPermissionDenied, URLConnectionError, AWSTokenError, SampleDataException
from .filters import DocumentFilter
from .models import Project, Label, Document, RoleMapping, Role, Comment, AutoLabelingConfig
from .permissions import IsProjectAdmin, IsAnnotatorAndReadOnly, IsAnnotator, IsAnnotationApproverAndReadOnly, IsOwnAnnotation, IsAnnotationApprover, IsOwnComment
from .serializers import ProjectSerializer, LabelSerializer, DocumentSerializer, UserSerializer, ApproverSerializer, CommentSerializer
from .serializers import ProjectPolymorphicSerializer, RoleMappingSerializer, RoleSerializer, AutoLabelingConfigSerializer
from .utils import CSVParser, ExcelParser, JSONParser, PlainTextParser, FastTextParser, CoNLLParser, AudioParser, iterable_to_io
from .utils import JSONLRenderer, PlainTextRenderer
from .utils import JSONPainter, CSVPainter, FastTextPainter

IsInProjectReadOnlyOrAdmin = (IsAnnotatorAndReadOnly | IsAnnotationApproverAndReadOnly | IsProjectAdmin)
IsInProjectOrAdmin = (IsAnnotator | IsAnnotationApprover | IsProjectAdmin)


class Health(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return Response({'status': 'green'})


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class Features(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({
            'cloud_upload': bool(settings.CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER),
        })


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectPolymorphicSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        return self.request.user.projects

    def perform_create(self, serializer):
        serializer.save(users=[self.request.user])


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_url_kwarg = 'project_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class StatisticsAPI(APIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get(self, request, *args, **kwargs):
        p = get_object_or_404(Project, pk=self.kwargs['project_id'])

        include = set(request.GET.getlist('include'))
        response = {}

        if not include or 'label' in include:
            label_count, user_count = self.label_per_data(p)
            response['label'] = label_count
            # TODO: Make user_label count chart
            response['user_label'] = user_count

        if not include or 'total' in include or 'remaining' in include or 'user' in include:
            progress = self.progress(project=p)
            response.update(progress)

        if include:
            response = {key: value for (key, value) in response.items() if key in include}

        return Response(response)

    @staticmethod
    def _get_user_completion_data(annotation_class, annotation_filter):
        all_annotation_objects  = annotation_class.objects.filter(annotation_filter)
        set_user_data = collections.defaultdict(set)
        for ind_obj in all_annotation_objects.values('user__username', 'document__id'):
            set_user_data[ind_obj['user__username']].add(ind_obj['document__id'])
        return {i: len(set_user_data[i]) for i in set_user_data}

    def progress(self, project):
        docs = project.documents
        annotation_class = project.get_annotation_class()
        total = docs.count()
        annotation_filter = Q(document_id__in=docs.all())
        user_data = self._get_user_completion_data(annotation_class, annotation_filter)
        if not project.collaborative_annotation:
            annotation_filter &= Q(user_id=self.request.user)
        done = annotation_class.objects.filter(annotation_filter)\
            .aggregate(Count('document', distinct=True))['document__count']
        remaining = total - done
        return {'total': total, 'remaining': remaining, 'user': user_data}

    def label_per_data(self, project):
        annotation_class = project.get_annotation_class()
        return annotation_class.objects.get_label_per_data(project=project)


class ApproveLabelsAPI(APIView):
    permission_classes = [IsAuthenticated & (IsAnnotationApprover | IsProjectAdmin)]

    def post(self, request, *args, **kwargs):
        approved = self.request.data.get('approved', True)
        document = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        document.annotations_approved_by = self.request.user if approved else None
        document.save()
        return Response(ApproverSerializer(document).data)


class LabelList(generics.ListCreateAPIView):
    serializer_class = LabelSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.labels

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    lookup_url_kwarg = 'label_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('text', )
    ordering_fields = ('created_at', 'updated_at', 'doc_annotations__updated_at',
                       'seq_annotations__updated_at', 'seq2seq_annotations__updated_at')
    filter_class = DocumentFilter
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])

        queryset = project.documents
        if project.randomize_document_order:
            random.seed(self.request.user.id)
            value = random.randrange(2, 20)
            queryset = queryset.annotate(sort_id=F('id') % value).order_by('sort_id', 'id')
        else:
            queryset = queryset.order_by('id')

        return queryset

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        queryset = project.documents
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_url_kwarg = 'doc_id'
    permission_classes = [IsAuthenticated & IsInProjectReadOnlyOrAdmin]


class AnnotationList(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
    swagger_schema = None

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()

        queryset = model.objects.filter(document=self.kwargs['doc_id'])
        if not project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def create(self, request, *args, **kwargs):
        self.check_single_class_classification(self.kwargs['project_id'], self.kwargs['doc_id'], request.user)

        request.data['document'] = self.kwargs['doc_id']
        return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        serializer.save(document_id=self.kwargs['doc_id'], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def check_single_class_classification(project_id, doc_id, user):
        project = get_object_or_404(Project, pk=project_id)
        if not project.single_class_classification:
            return

        model = project.get_annotation_class()
        annotations = model.objects.filter(document_id=doc_id)
        if not project.collaborative_annotation:
            annotations = annotations.filter(user=user)

        if annotations.exists():
            raise ValidationError('requested to create duplicate annotation for single-class-classification project')


class AnnotationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'annotation_id'
    swagger_schema = None

    def get_permissions(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        if project.collaborative_annotation:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated & IsInProjectOrAdmin & IsOwnAnnotation]
        return super().get_permissions()

    def get_serializer_class(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        self.serializer_class = project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()
        self.queryset = model.objects.all()
        return self.queryset


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin]

    def get_queryset(self):
        return Comment.objects.filter(
            document_id=self.kwargs['doc_id'],
            user_id=self.request.user.id,
        ).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, document_id=self.kwargs['doc_id'])


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = [IsAuthenticated & IsInProjectOrAdmin & IsOwnComment]


class TextUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')

        self.save_file(
            user=request.user,
            file=request.data['file'],
            file_format=request.data['format'],
            project_id=kwargs['project_id'],
        )

        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def save_file(cls, user, file, file_format, project_id):
        project = get_object_or_404(Project, pk=project_id)
        parser = cls.select_parser(file_format)
        data = parser.parse(file)
        storage = project.get_storage(data)
        storage.save(user)

    @classmethod
    def select_parser(cls, file_format):
        if file_format == 'plain':
            return PlainTextParser()
        elif file_format == 'csv':
            return CSVParser()
        elif file_format == 'json':
            return JSONParser()
        elif file_format == 'conll':
            return CoNLLParser()
        elif file_format == 'excel':
            return ExcelParser()
        elif file_format == 'audio':
            return AudioParser()
        elif file_format == 'fastText':
            return FastTextParser()
        else:
            raise ValidationError('format {} is invalid.'.format(file_format))


class CloudUploadAPI(APIView):
    permission_classes = TextUploadAPI.permission_classes

    def get(self, request, *args, **kwargs):
        try:
            project_id = request.query_params['project_id']
            file_format = request.query_params['upload_format']
            cloud_container = request.query_params['container']
            cloud_object = request.query_params['object']
        except KeyError as ex:
            raise ValidationError('query parameter {} is missing'.format(ex))

        try:
            cloud_file = self.get_cloud_object_as_io(cloud_container, cloud_object)
        except ContainerDoesNotExistError:
            raise ValidationError('cloud container {} does not exist'.format(cloud_container))
        except ObjectDoesNotExistError:
            raise ValidationError('cloud object {} does not exist'.format(cloud_object))

        TextUploadAPI.save_file(
            user=request.user,
            file=cloud_file,
            file_format=file_format,
            project_id=project_id,
        )

        next_url = request.query_params.get('next')

        if next_url == 'about:blank':
            return Response(data='', content_type='text/plain', status=status.HTTP_201_CREATED)

        if next_url:
            return redirect(next_url)

        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def get_cloud_object_as_io(cls, container_name, object_name):
        provider = settings.CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER.lower()
        account = settings.CLOUD_BROWSER_APACHE_LIBCLOUD_ACCOUNT
        key = settings.CLOUD_BROWSER_APACHE_LIBCLOUD_SECRET_KEY

        driver = get_driver(DriverType.STORAGE, provider)
        client = driver(account, key)

        cloud_container = client.get_container(container_name)
        cloud_object = cloud_container.get_object(object_name)

        return iterable_to_io(cloud_object.as_stream())


class TextDownloadAPI(APIView):
    permission_classes = TextUploadAPI.permission_classes

    renderer_classes = (CSVRenderer, JSONLRenderer, PlainTextRenderer)

    def get(self, request, *args, **kwargs):
        format = request.query_params.get('q')
        only_approved = request.query_params.get('onlyApproved')
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        documents = (
            project.documents.exclude(annotations_approved_by = None)
            if only_approved == 'true'
            else project.documents.all()
        )
        painter = self.select_painter(format)

        # jsonl-textlabel format prints text labels while jsonl format prints annotations with label ids
        # jsonl-textlabel format - "labels": [[0, 15, "PERSON"], ..]
        # jsonl format - "annotations": [{"label": 5, "start_offset": 0, "end_offset": 2, "user": 1},..]
        if format in ('jsonl', 'txt'):
            labels = project.labels.all()
            data = painter.paint_labels(documents, labels)
        else:
            data = painter.paint(documents)
        return Response(data)

    def select_painter(self, format):
        if format == 'csv':
            return CSVPainter()
        elif format == 'jsonl' or format == 'json':
            return JSONPainter()
        elif format == 'txt':
            return FastTextPainter()
        else:
            raise ValidationError('format {} is invalid.'.format(format))


class Users(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serialized_data = UserSerializer(queryset, many=True).data
        return Response(serialized_data)


class Roles(generics.ListCreateAPIView):
    serializer_class = RoleSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    queryset = Role.objects.all()


class RoleMappingList(generics.ListCreateAPIView):
    serializer_class = RoleMappingSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return project.role_mappings

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)


class RoleMappingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleMapping.objects.all()
    serializer_class = RoleMappingSerializer
    lookup_url_kwarg = 'rolemapping_id'
    permission_classes = [IsAuthenticated & IsProjectAdmin]


class LabelUploadAPI(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ParseError('Empty content')
        labels = json.load(request.data['file'])
        project = get_object_or_404(Project, pk=kwargs['project_id'])
        try:
            for label in labels:
                serializer = LabelSerializer(data=label)
                serializer.is_valid(raise_exception=True)
                serializer.save(project=project)
            return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            content = {'error': 'IntegrityError: you cannot create a label with same name or shortkey.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


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

    def post(self, *args, **kwargs):
        model_name = self.request.data['model_name']
        model_attrs = self.request.data['model_attrs']
        sample_text = self.request.data['text']
        try:
            model = RequestModelFactory.create(model_name, model_attrs)
        except Exception:
            model = RequestModelFactory.find(model_name)
            schema = model.schema()
            required_fields = ', '.join(schema['required']) if 'required' in schema else ''
            raise ValidationError(
                'The attributes does not match the model.'
                'You need to correctly specify the required fields: {}'.format(required_fields)
            )
        try:
            request = model.build()
            response = request.send(text=sample_text)
            return Response(response, status=status.HTTP_200_OK)
        except requests.exceptions.ConnectionError:
            raise URLConnectionError
        except botocore.exceptions.ClientError:
            raise AWSTokenError()
        except Exception as e:
            raise e


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
        labels = template.render(response)
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
        self.serializer_class = project.get_annotation_serializer()
        return self.serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        model = project.get_annotation_class()
        queryset = model.objects.filter(document=self.kwargs['doc_id'])
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

    def extract(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        doc = get_object_or_404(Document, pk=self.kwargs['doc_id'])
        config = project.auto_labeling_config.first()
        if not config:
            raise AutoLabeliingPermissionDenied()
        return execute_pipeline(
            text=doc.text,
            project_type=project.project_type,
            model_name=config.model_name,
            model_attrs=config.model_attrs,
            template=config.template,
            label_mapping=config.label_mapping
        )

    def transform(self, labels):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        for label in labels:
            label['document'] = self.kwargs['doc_id']
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
