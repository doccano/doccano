from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Project
from .views.download.factory import create_repository, create_writer
from .views.download.service import ExportApplicationService
from .views.upload.factories import (create_bulder, create_cleaner,
                                     create_parser)
from .views.upload.readers import Reader
from .views.upload.writers import BulkWriter

logger = get_task_logger(__name__)


@shared_task
def ingest_data(user_id, project_id, filenames, format: str, **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)

    parser = create_parser(format, **kwargs)
    builder = create_bulder(project, **kwargs)
    reader = Reader(filenames=filenames, parser=parser, builder=builder)
    cleaner = create_cleaner(project)
    writer = BulkWriter(batch_size=settings.IMPORT_BATCH_SIZE)
    writer.save(reader, project, user, cleaner)
    return {'error': writer.errors}


@shared_task
def export_dataset(project_id, format: str, export_approved=False):
    project = get_object_or_404(Project, pk=project_id)
    repository = create_repository(project)
    writer = create_writer(format)(settings.MEDIA_ROOT)
    service = ExportApplicationService(repository, writer)
    filepath = service.export(export_approved)
    return filepath
