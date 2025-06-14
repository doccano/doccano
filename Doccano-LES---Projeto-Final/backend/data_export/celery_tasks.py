import os
import shutil
import uuid

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.shortcuts import get_object_or_404

from .pipeline.dataset import Dataset
from .pipeline.factories import (
    create_comment,
    create_formatter,
    create_labels,
    create_writer,
)
from .pipeline.services import ExportApplicationService
from data_export.models import ExportedExample
from projects.models import Member, Project

logger = get_task_logger(__name__)


def create_collaborative_dataset(project: Project, dirpath: str, confirmed_only: bool, formatters, writer):
    is_text_project = project.is_text_project
    if confirmed_only:
        examples = ExportedExample.objects.confirmed(project)
    else:
        examples = ExportedExample.objects.filter(project=project)
    labels = create_labels(project, examples)
    comments = create_comment(examples)
    dataset = Dataset(examples, labels, comments, is_text_project)

    service = ExportApplicationService(dataset, formatters, writer)

    filepath = os.path.join(dirpath, f"all.{writer.extension}")
    service.export(filepath)


def create_individual_dataset(project: Project, dirpath: str, confirmed_only: bool, formatters, writer):
    is_text_project = project.is_text_project
    members = Member.objects.filter(project=project)
    for member in members:
        if confirmed_only:
            examples = ExportedExample.objects.confirmed(project, user=member.user)
        else:
            examples = ExportedExample.objects.filter(project=project)
        labels = create_labels(project, examples, member.user)
        comments = create_comment(examples, member.user)
        dataset = Dataset(examples, labels, comments, is_text_project)

        service = ExportApplicationService(dataset, formatters, writer)

        filepath = os.path.join(dirpath, f"{member.username}.{writer.extension}")
        service.export(filepath)


@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def export_dataset(project_id, file_format: str, confirmed_only=False):
    project = get_object_or_404(Project, pk=project_id)
    dirpath = os.path.join(settings.MEDIA_ROOT, str(uuid.uuid4()))
    os.makedirs(dirpath, exist_ok=True)
    formatters = create_formatter(project, file_format)
    writer = create_writer(file_format)
    if project.collaborative_annotation:
        create_collaborative_dataset(project, dirpath, confirmed_only, formatters, writer)
    else:
        create_individual_dataset(project, dirpath, confirmed_only, formatters, writer)
    zip_file = shutil.make_archive(dirpath, "zip", dirpath)
    shutil.rmtree(dirpath)
    return zip_file
