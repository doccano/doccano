import itertools
from typing import List

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Example, Label, Project
from .views.download.factory import create_repository, create_writer
from .views.download.service import ExportApplicationService
from .views.upload.exception import FileParseException, FileParseExceptions
from .views.upload.factory import (create_cleaner, get_data_class,
                                   get_dataset_class, get_label_class)

logger = get_task_logger(__name__)


def group_by_class(instances):
    from collections import defaultdict
    groups = defaultdict(list)
    for instance in instances:
        groups[instance.__class__].append(instance)
    return groups


class Examples:

    def __init__(self, buffer_size=settings.IMPORT_BATCH_SIZE):
        self.buffer_size = buffer_size
        self.buffer = []

    def __len__(self):
        return len(self.buffer)

    @property
    def data(self):
        return self.buffer

    def add(self, data):
        self.buffer.append(data)

    def clear(self):
        self.buffer = []

    def is_full(self):
        return len(self) >= self.buffer_size

    def is_empty(self):
        return len(self) == 0

    def save_label(self, project: Project):
        labels = list(itertools.chain.from_iterable([example.create_label(project) for example in self.buffer]))
        labels = list(filter(None, labels))
        Label.objects.bulk_create(labels, ignore_conflicts=True)

    def save_data(self, project: Project) -> List[Example]:
        examples = [example.create_data(project) for example in self.buffer]
        return Example.objects.bulk_create(examples)

    def save_annotation(self, project, user, examples):
        mapping = {(label.text, label.task_type): label for label in project.labels.all()}
        annotations = list(itertools.chain.from_iterable([
            data.create_annotation(user, example, mapping) for data, example in zip(self.buffer, examples)
        ]))
        groups = group_by_class(annotations)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances)


class DataFactory:

    def create(self, examples, user, project):
        examples.save_label(project)
        ids = examples.save_data(project)
        examples.save_annotation(project, user, ids)


@shared_task
def ingest_data(user_id, project_id, filenames, format: str, **kwargs):
    project = get_object_or_404(Project, pk=project_id)
    user = get_object_or_404(get_user_model(), pk=user_id)
    response = {'error': []}

    # Prepare dataset.
    dataset_class = get_dataset_class(format)
    dataset = dataset_class(
        filenames=filenames,
        label_class=get_label_class(project.project_type),
        data_class=get_data_class(project.project_type),
        **kwargs
    )
    it = iter(dataset)
    buffer = Examples()
    factory = DataFactory()
    cleaner = create_cleaner(project)
    while True:
        try:
            example = next(it)
        except StopIteration:
            break
        except FileParseException as err:
            response['error'].append(err.dict())
            continue
        except FileParseExceptions as err:
            response['error'].extend(list(err))
            continue
        try:
            example.clean(cleaner)
        except FileParseException as err:
            response['error'].append(err.dict())

        buffer.add(example)
        if buffer.is_full():
            factory.create(buffer, user, project)
            buffer.clear()
    if not buffer.is_empty():
        logger.debug(f'BUFFER LEN {len(buffer)}')
        factory.create(buffer, user, project)
        buffer.clear()

    return response


@shared_task
def export_dataset(project_id, format: str, export_approved=False):
    project = get_object_or_404(Project, pk=project_id)
    repository = create_repository(project)
    writer = create_writer(format)(settings.MEDIA_ROOT)
    service = ExportApplicationService(repository, writer)
    filepath = service.export(export_approved)
    return filepath
