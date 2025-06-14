from django.shortcuts import get_object_or_404
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
        use_relation = getattr(project, "use_relation", False)
        options = Options.filter_by_task(project.project_type, use_relation)
        return Response(data=options, status=status.HTTP_200_OK)


class DatasetImportAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, request, *args, **kwargs):
        upload_ids = request.data.pop("uploadIds")
        file_format = request.data.pop("format")
        task = request.data.pop("task")
        celery_task = import_dataset.delay(
            user_id=request.user.id,
            project_id=self.kwargs["project_id"],
            file_format=file_format,
            upload_ids=upload_ids,
            task=task,
            **request.data,
        )
        return Response({"task_id": celery_task.task_id})
