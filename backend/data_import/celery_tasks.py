from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from projects.models import Project
from .pipeline.factories import create_parser, create_builder, create_cleaner
from .pipeline.readers import Reader
from .pipeline.writers import BulkWriter


@shared_task
def import_dataset(user_id, project_id, filenames, file_format: str, **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)

    parser = create_parser(file_format, **kwargs)
    builder = create_builder(project, **kwargs)
    reader = Reader(filenames=filenames, parser=parser, builder=builder)
    cleaner = create_cleaner(project)
    writer = BulkWriter(batch_size=settings.IMPORT_BATCH_SIZE)
    writer.save(reader, project, user, cleaner)
    return {"error": writer.errors}
