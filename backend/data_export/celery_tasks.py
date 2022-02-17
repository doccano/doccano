from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.shortcuts import get_object_or_404

from .pipeline.factories import create_repository, create_writer
from .pipeline.services import ExportApplicationService
from projects.models import Project

logger = get_task_logger(__name__)


@shared_task
def export_dataset(project_id, file_format: str, export_approved=False):
    project = get_object_or_404(Project, pk=project_id)
    repository = create_repository(project)
    writer = create_writer(file_format)(settings.MEDIA_ROOT)
    service = ExportApplicationService(repository, writer)
    filepath = service.export(export_approved)
    return filepath
