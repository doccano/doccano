import os

from django.shortcuts import get_object_or_404
from django_drf_filepond.api import store_upload
from django_drf_filepond.models import TemporaryUpload
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Project
from ..permissions import IsProjectAdmin
from ..tasks import injest_data
from .upload.catalog import Options


class DatasetCatalog(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        options = Options.filter_by_task(project.project_type)
        return Response(data=options, status=status.HTTP_200_OK)


class UploadAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        upload_ids = request.data.pop('uploadIds')
        format = request.data.pop('format')

        tus = [TemporaryUpload.objects.get(upload_id=upload_id) for upload_id in upload_ids]
        sus = [
            store_upload(
                tu.upload_id,
                destination_file_path=os.path.join(tu.file.name, tu.upload_name)
            )
            for tu in tus
        ]
        filenames = [su.file.path for su in sus]
        task = injest_data.delay(
            user_id=request.user.id,
            project_id=project_id,
            filenames=filenames,
            format=format,
            **request.data
        )
        return Response({'task_id': task.task_id})
