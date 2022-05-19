from celery.result import AsyncResult
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .celery_tasks import export_dataset
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


class DatasetExportAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        task_id = request.GET["taskId"]
        task = AsyncResult(task_id)
        ready = task.ready()
        if ready:
            filename = task.result
            return FileResponse(open(filename, mode="rb"), as_attachment=True)
        return Response({"status": "Not ready"})

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs["project_id"]
        file_format = request.data.pop("format")
        export_approved = request.data.pop("exportApproved", False)
        task = export_dataset.delay(
            project_id=project_id, file_format=file_format, confirmed_only=export_approved, **request.data
        )
        return Response({"task_id": task.task_id})
