from typing import List

import filetype
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_drf_filepond.api import store_upload
from django_drf_filepond.models import TemporaryUpload

from .datasets import load_dataset
from .pipeline.catalog import Format, create_file_format
from .pipeline.exceptions import (
    FileImportException,
    FileTypeException,
    MaximumFileSizeException,
)
from .pipeline.readers import FileName
from projects.models import Project


def check_file_type(filename, file_format: Format, filepath: str):
    if not settings.ENABLE_FILE_TYPE_CHECK:
        return
    kind = filetype.guess(filepath)
    if not file_format.validate_mime(kind.mime):
        raise FileTypeException(filename, kind.mime, file_format.accept_types)


def check_uploaded_files(upload_ids: List[str], file_format: Format):
    errors: List[FileImportException] = []
    cleaned_ids = []
    temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
    for tu in temporary_uploads:
        if tu.file.size > settings.MAX_UPLOAD_SIZE:
            errors.append(MaximumFileSizeException(tu.upload_name, settings.MAX_UPLOAD_SIZE))
            tu.delete()
            continue
        try:
            check_file_type(tu.upload_name, file_format, tu.get_file_path())
        except FileTypeException as e:
            errors.append(e)
            tu.delete()
            continue
        cleaned_ids.append(tu.upload_id)
    return cleaned_ids, errors


@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def import_dataset(user_id, project_id, file_format: str, upload_ids: List[str], task: str, **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)
    try:
        fmt = create_file_format(file_format)
        upload_ids, errors = check_uploaded_files(upload_ids, fmt)
        temporary_uploads = TemporaryUpload.objects.filter(upload_id__in=upload_ids)
        filenames = [
            FileName(full_path=tu.get_file_path(), generated_name=tu.file.name, upload_name=tu.upload_name)
            for tu in temporary_uploads
        ]

        dataset = load_dataset(task, fmt, filenames, project, **kwargs)
        dataset.save(user, batch_size=settings.IMPORT_BATCH_SIZE)
        upload_to_store(temporary_uploads)
        errors.extend(dataset.errors)
        return {"error": [e.dict() for e in errors]}
    except FileImportException as e:
        return {"error": [e.dict()]}


def upload_to_store(temporary_uploads):
    for tu in temporary_uploads:
        store_upload(tu.upload_id, destination_file_path=tu.file.name)
