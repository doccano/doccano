from typing import List

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_drf_filepond.api import store_upload
from django_drf_filepond.models import TemporaryUpload

from .pipeline.factories import create_builder, create_cleaner, create_parser
from .pipeline.readers import Reader
from .pipeline.writers import BulkWriter
from projects.models import Project


@shared_task
def import_dataset(user_id, project_id, file_format: str, upload_ids: List[str], **kwargs):
    temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
    file_names = [tu.get_file_path() for tu in temporary_uploads]
    save_names = {tu.get_file_path(): tu.file.name for tu in temporary_uploads}

    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)

    parser = create_parser(file_format, **kwargs)
    builder = create_builder(project, **kwargs)
    reader = Reader(filenames=file_names, parser=parser, builder=builder)
    cleaner = create_cleaner(project)
    writer = BulkWriter(batch_size=settings.IMPORT_BATCH_SIZE, save_names=save_names)
    writer.save(reader, project, user, cleaner)
    return {"error": writer.errors}


@shared_task
def upload_to_store(upload_ids: List[int]):
    temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
    for tu in temporary_uploads:
        store_upload(tu.upload_id, destination_file_path=tu.file.name)
