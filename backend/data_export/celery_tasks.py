import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import ExportedExample
from .pipeline.dataset import Dataset, filter_examples
from .pipeline.factories import (
    create_labels,
    select_formatter,
    select_label_collection,
    select_writer,
)
from .pipeline.services import ExportApplicationService
from .pipeline.writers import zip_files
from projects.models import Member, Project

logger = get_task_logger(__name__)


def create_collaborative_dataset(project: Project, file_format: str, confirmed_only: bool):
    examples = filter_examples(
        examples=ExportedExample.objects.filter(project=project),
        is_collaborative=project.collaborative_annotation,
        confirmed_only=confirmed_only,
    )
    writer = select_writer(file_format)()
    label_collections = select_label_collection(project)
    formatter_classes = select_formatter(project, file_format)
    formatters = [
        formatter(target_column=label_collection.field_name)
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
        examples = filter_examples(
            examples=ExportedExample.objects.filter(project=project),
            is_collaborative=project.collaborative_annotation,
            confirmed_only=confirmed_only,
            user=member.user,
        )
        writer = select_writer(file_format)()
        label_collections = select_label_collection(project)
        formatter_classes = select_formatter(project, file_format)
        formatters = [
            formatter(target_column=label_collection.field_name)
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
    for file in files:
        os.remove(file)
    return zip_file


@shared_task
def export_dataset(project_id, file_format: str, export_approved=False):
    project = get_object_or_404(Project, pk=project_id)
    if project.collaborative_annotation:
        return create_collaborative_dataset(project, file_format, export_approved)
    else:
        return create_individual_dataset(project, file_format, export_approved)
