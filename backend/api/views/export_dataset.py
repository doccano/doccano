from celery.result import AsyncResult
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Project
from ..permissions import IsProjectAdmin
from ..tasks import export_dataset
from .download.catalog import Options


class DownloadDatasetCatalog(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        project = get_object_or_404(Project, pk=project_id)
        options = Options.filter_by_task(project.project_type)
        return Response(data=options, status=status.HTTP_200_OK)


class DownloadAPI(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def get(self, request, *args, **kwargs):
        task_id = request.GET['taskId']
        task = AsyncResult(task_id)
        ready = task.ready()
        if ready:
            filename = task.result
            return FileResponse(open(filename, mode='rb'), as_attachment=True)

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        format = request.data.pop('format')
        export_approved = request.data.pop('exportApproved', False)
        task = export_dataset.delay(
            project_id=project_id,
            format=format,
            export_approved=export_approved,
            **request.data
        )
        return Response({'task_id': task.task_id})
