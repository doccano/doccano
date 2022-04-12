from typing import List

import filetype
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_drf_filepond.api import store_upload
from django_drf_filepond.models import TemporaryUpload

from .pipeline.catalog import AudioFile, ImageFile
from .pipeline.exceptions import FileTypeException, MaximumFileSizeException
from .pipeline.factories import create_builder, create_cleaner, create_parser
from .pipeline.readers import FileName, Reader
from .pipeline.writers import BulkWriter
from projects.models import Project


def check_file_type(filename, file_format: str, filepath: str):
    if not settings.ENABLE_FILE_TYPE_CHECK:
        return
    kind = filetype.guess(filepath)
    if file_format == ImageFile.name:
        accept_types = ImageFile.accept_types.replace(" ", "").split(",")
    elif file_format == AudioFile.name:
        accept_types = AudioFile.accept_types.replace(" ", "").split(",")
    else:
        return
    if kind.mime not in accept_types:
        raise FileTypeException(filename, kind.mime, accept_types)


def check_uploaded_files(upload_ids: List[str], file_format: str):
    errors = []
    cleaned_ids = []
    temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
    for tu in temporary_uploads:
        if tu.file.size > settings.MAX_UPLOAD_SIZE:
            errors.append(MaximumFileSizeException(tu.upload_name, settings.MAX_UPLOAD_SIZE).dict())
            tu.delete()
            continue
        try:
            check_file_type(tu.upload_name, file_format, tu.get_file_path())
        except FileTypeException as e:
            errors.append(e.dict())
        cleaned_ids.append(tu.upload_id)
    return cleaned_ids, errors


@shared_task
def import_dataset(user_id, project_id, file_format: str, upload_ids: List[str], **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)

    upload_ids, errors = check_uploaded_files(upload_ids, file_format)
    temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
    filenames = [
        FileName(full_path=tu.get_file_path(), generated_name=tu.file.name, upload_name=tu.upload_name)
        for tu in temporary_uploads
    ]

    parser = create_parser(file_format, **kwargs)
    builder = create_builder(project, **kwargs)
    reader = Reader(filenames=filenames, parser=parser, builder=builder)
    cleaner = create_cleaner(project)
    writer = BulkWriter(batch_size=settings.IMPORT_BATCH_SIZE)
    writer.save(reader, project, user, cleaner)
    upload_to_store(temporary_uploads)
    return {"error": writer.errors + errors}


def upload_to_store(temporary_uploads):
    for tu in temporary_uploads:
        store_upload(tu.upload_id, destination_file_path=tu.file.name)
