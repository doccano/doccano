from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from libcloud import DriverType, get_driver
from libcloud.storage.types import (ContainerDoesNotExistError,
                                    ObjectDoesNotExistError)
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer

from ..models import Project
from ..permissions import IsProjectAdmin
from ..utils import (AudioParser, CoNLLParser, CSVPainter, CSVParser,
                     ExcelParser, FastTextPainter, FastTextParser,
                     JSONLRenderer, JSONPainter, JSONParser, PlainTextParser,
                     PlainTextRenderer, iterable_to_io)


class Features(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({
            'cloud_upload': bool(settings.CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER),
        })


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
