import abc
import itertools
from collections import defaultdict
from typing import List

from django.conf import settings

from ...models import Example, Label, Project
from .exception import FileParseException
from .readers import BaseReader


class Writer(abc.ABC):

    @abc.abstractmethod
    def save(self, reader: BaseReader, project: Project, user, cleaner):
        """Save the read contents to DB."""
        raise NotImplementedError('Please implement this method in the subclass.')


def group_by_class(instances):
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


class BulkWriter(Writer):

    def __init__(self, batch_size):
        self.examples = Examples(batch_size)
        self._errors = []

    def save(self, reader: BaseReader, project, user, cleaner):
        it = iter(reader)
        while True:
            try:
                example = next(it)
            except StopIteration:
                break
            try:
                example.clean(cleaner)
            except FileParseException as err:
                self._errors.append(err)

            self.examples.add(example)
            if self.examples.is_full():
                self.create(project, user)
                self.examples.clear()
        if not self.examples.is_empty():
            self.create(project, user)
            self.examples.clear()
        self._errors.extend(reader.errors)

    @property
    def errors(self) -> List[FileParseException]:
        self._errors.sort(key=lambda e: e.line_num)
        return self._errors

    def create(self, project, user):
        self.examples.save_label(project)
        ids = self.examples.save_data(project)
        self.examples.save_annotation(project, user, ids)
