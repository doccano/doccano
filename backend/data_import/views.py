import os

from django.shortcuts import get_object_or_404
from django_drf_filepond.api import store_upload
from django_drf_filepond.models import TemporaryUpload
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .celery_tasks import import_dataset
from .pipeline.catalog import Options
from projects.models import Project
from projects.permissions import IsProjectAdmin


class DatasetCatalog(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        project = get_object_or_404(Project, pk=project_id)
        options = Options.filter_by_task(project.project_type)
        return Response(data=options, status=status.HTTP_200_OK)


class DatasetImportAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        upload_ids = request.data.pop("uploadIds")
        file_format = request.data.pop("format")

        tus = [TemporaryUpload.objects.get(upload_id=upload_id) for upload_id in upload_ids]
        sus = [
            store_upload(tu.upload_id, destination_file_path=os.path.join(tu.file.name, tu.upload_name)) for tu in tus
        ]
        filenames = [su.file.path for su in sus]
        task = import_dataset.delay(
            user_id=request.user.id, project_id=project_id, filenames=filenames, file_format=file_format, **request.data
        )
        return Response({"task_id": task.task_id})
