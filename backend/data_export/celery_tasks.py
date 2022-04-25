import os
import shutil
import uuid

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.shortcuts import get_object_or_404

from .pipeline.dataset import Dataset
from .pipeline.factories import create_formatter, create_labels, create_writer
from .pipeline.services import ExportApplicationService
from data_export.models import ExportedExample
from projects.models import Member, Project

logger = get_task_logger(__name__)


def create_collaborative_dataset(project: Project, file_format: str, confirmed_only: bool):
    if confirmed_only:
        examples = ExportedExample.objects.confirmed(project)
    else:
        examples = ExportedExample.objects.filter(project=project)
    is_text_project = project.is_text_project
    labels = create_labels(project, examples)
    dataset = Dataset(examples, labels, is_text_project)

    formatters = create_formatter(project, file_format)
    writer = create_writer(file_format)
    service = ExportApplicationService(dataset, formatters, writer)
    dirname = str(uuid.uuid4())
    dirpath = os.path.join(settings.MEDIA_ROOT, dirname)
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, f"all.{writer.extension}")
    service.export(filepath)
    zip_file = shutil.make_archive(dirpath, "zip", dirpath)
    shutil.rmtree(dirpath)
    return zip_file


def create_individual_dataset(project: Project, file_format: str, confirmed_only: bool):
    members = Member.objects.filter(project=project)
    is_text_project = project.is_text_project
    dirname = str(uuid.uuid4())
    dirpath = os.path.join(settings.MEDIA_ROOT, dirname)
    os.makedirs(dirpath, exist_ok=True)
    for member in members:
        if confirmed_only:
            examples = ExportedExample.objects.confirmed(project, user=member.user)
        else:
            examples = ExportedExample.objects.filter(project=project)
        labels = create_labels(project, examples, member.user)
        dataset = Dataset(examples, labels, is_text_project)

        formatters = create_formatter(project, file_format)
        writer = create_writer(file_format)
        service = ExportApplicationService(dataset, formatters, writer)
        filepath = os.path.join(dirpath, f"{member.username}.{writer.extension}")
        service.export(filepath)
    zip_file = shutil.make_archive(dirpath, "zip", dirpath)
    shutil.rmtree(dirpath)
    return zip_file


@shared_task
def export_dataset(project_id, file_format: str, confirmed_only=False):
    project = get_object_or_404(Project, pk=project_id)
    if project.collaborative_annotation:
        return create_collaborative_dataset(project, file_format, confirmed_only)
    else:
        return create_individual_dataset(project, file_format, confirmed_only)
