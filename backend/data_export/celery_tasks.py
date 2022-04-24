import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.shortcuts import get_object_or_404

from .pipeline.dataset import Dataset
from .pipeline.factories import (
    create_labels,
    select_formatter,
    select_label_collection,
    select_writer,
)
from .pipeline.services import ExportApplicationService
from .pipeline.writers import remove_files, zip_files
from data_export.models import ExportedExample
from projects.models import Member, Project

logger = get_task_logger(__name__)


def create_collaborative_dataset(project: Project, file_format: str, confirmed_only: bool):
    if confirmed_only:
        examples = ExportedExample.objects.confirmed(is_collaborative=project.collaborative_annotation)
    else:
        examples = ExportedExample.objects.all()
    writer = select_writer(file_format)()
    label_collections = select_label_collection(project)
    formatter_classes = select_formatter(project, file_format)
    formatters = [
        formatter(target_column=label_collection.column)
        for formatter, label_collection in zip(formatter_classes, label_collections)
    ]
    labels = [create_labels(label_collection, examples=examples) for label_collection in label_collections]
    dataset = Dataset(examples, labels)

    service = ExportApplicationService(dataset, formatters, writer)
    filepath = os.path.join(settings.MEDIA_URL, f"all.{writer.extension}")
    service.export(filepath)
    return filepath


def create_individual_dataset(project: Project, file_format: str, confirmed_only: bool):
    files = []
    members = Member.objects.filter(project=project)
    for member in members:
        if confirmed_only:
            examples = ExportedExample.objects.confirmed(
                is_collaborative=project.collaborative_annotation, user=member.user
            )
        else:
            examples = ExportedExample.objects.all()
        writer = select_writer(file_format)()
        label_collections = select_label_collection(project)
        formatter_classes = select_formatter(project, file_format)
        formatters = [
            formatter(target_column=label_collection.column)
            for formatter, label_collection in zip(formatter_classes, label_collections)
        ]
        labels = [
            create_labels(label_collection, examples=examples, user=member.user)
            for label_collection in label_collections
        ]
        dataset = Dataset(examples, labels)

        service = ExportApplicationService(dataset, formatters, writer)
        filepath = os.path.join(settings.MEDIA_URL, f"{member.username}.{writer.extension}")
        service.export(filepath)
        files.append(filepath)
    zip_file = zip_files(files, settings.MEDIA_URL)
    remove_files(files)
    return zip_file


@shared_task
def export_dataset(project_id, file_format: str, export_approved=False):
    project = get_object_or_404(Project, pk=project_id)
    if project.collaborative_annotation:
        return create_collaborative_dataset(project, file_format, export_approved)
    else:
        return create_individual_dataset(project, file_format, export_approved)
