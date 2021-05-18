import datetime
import itertools

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Example, Label, Project
from .views.download.factory import create_repository, create_writer
from .views.download.service import ExportApplicationService
from .views.upload.exception import FileParseException
from .views.upload.factory import (get_data_class, get_dataset_class,
                                   get_label_class)
from .views.upload.utils import append_field


class Buffer:

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


class DataFactory:

    def __init__(self, data_class, label_class, annotation_class):
        self.data_class = data_class
        self.label_class = label_class
        self.annotation_class = annotation_class

    def create_label(self, examples, project):
        flatten = itertools.chain(*[example.label for example in examples])
        labels = {
            label['text'] for label in flatten
            if not project.labels.filter(text=label['text']).exists()
        }
        labels = [self.label_class(text=text, project=project) for text in labels]
        self.label_class.objects.bulk_create(labels)

    def create_data(self, examples, project):
        dataset = [
            self.data_class(project=project, **example.data)
            for example in examples
        ]
        now = datetime.datetime.now()
        self.data_class.objects.bulk_create(dataset)
        ids = self.data_class.objects.filter(created_at__gte=now)
        return list(ids)

    def create_annotation(self, examples, ids, user, project):
        mapping = {label.text: label.id for label in project.labels.all()}
        annotation = [example.annotation(mapping) for example in examples]
        for a, id in zip(annotation, ids):
            append_field(a, example=id)
        annotation = list(itertools.chain(*annotation))
        for a in annotation:
            if 'label' in a:
                a['label_id'] = a.pop('label')
        annotation = [self.annotation_class(**a, user=user) for a in annotation]
        self.annotation_class.objects.bulk_create(annotation)

    def create(self, examples, user, project):
        self.create_label(examples, project)
        ids = self.create_data(examples, project)
        self.create_annotation(examples, ids, user, project)


@shared_task
def injest_data(user_id, project_id, filenames, format: str, **kwargs):
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
    buffer = Buffer()
    factory = DataFactory(
        data_class=Example,
        label_class=Label,
        annotation_class=project.get_annotation_class()
    )
    while True:
        try:
            example = next(it)
        except StopIteration:
            break
        except FileParseException as err:
            response['error'].append(err.dict())
            continue

        buffer.add(example)
        if buffer.is_full():
            factory.create(buffer.data, user, project)
            buffer.clear()
    if not buffer.is_empty():
        factory.create(buffer.data, user, project)
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
