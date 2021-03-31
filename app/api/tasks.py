from celery import shared_task
from django.conf import settings
from django_drf_filepond.api import store_upload
from django_drf_filepond.models import TemporaryUpload

from .models import Document, Label


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def parse(upload_id):
    tu = TemporaryUpload.objects.get(upload_id=upload_id)
    su = store_upload(upload_id, destination_file_path=tu.upload_name)
    return su.file.path
