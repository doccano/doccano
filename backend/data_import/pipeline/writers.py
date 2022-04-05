import abc
import itertools
from collections import defaultdict
from typing import Any, Dict, List, Type

from django.conf import settings

from .exceptions import FileParseException
from .readers import BaseReader, Record
from examples.models import Example
from label_types.models import CategoryType, LabelType, SpanType
from projects.models import Project


class Writer(abc.ABC):
    @abc.abstractmethod
    def save(self, reader: BaseReader, project: Project, user, cleaner):
        """Save the read contents to DB."""
        raise NotImplementedError("Please implement this method in the subclass.")

    def errors(self) -> List[Dict[Any, Any]]:
        """Return errors."""
        raise NotImplementedError("Please implement this method in the subclass.")


def group_by_class(instances):
    groups = defaultdict(list)
    for instance in instances:
        groups[instance.__class__].append(instance)
    return groups


class Examples:
    def __init__(self, buffer_size: int = settings.IMPORT_BATCH_SIZE):
        self.buffer_size = buffer_size
        self.buffer: List[Record] = []

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
        groups = group_by_class(labels)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances, ignore_conflicts=True)

    def save_data(self, project: Project) -> List[Example]:
        examples = [example.create_data(project) for example in self.buffer]
        return Example.objects.bulk_create(examples)

    def save_annotation(self, project: Project, user, examples):
        # Todo: move annotation class
        mapping = {}
        label_types: List[Type[LabelType]] = [CategoryType, SpanType]
        for model in label_types:
            for label in model.objects.filter(project=project):
                mapping[label.text] = label
        annotations = list(
            itertools.chain.from_iterable(
                [data.create_annotation(user, example, mapping) for data, example in zip(self.buffer, examples)]
            )
        )
        groups = group_by_class(annotations)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances)


class BulkWriter(Writer):
    def __init__(self, batch_size: int):
        self.examples = Examples(batch_size)
        self._errors: List[FileParseException] = []

    def save(self, reader: BaseReader, project: Project, user, cleaner):
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
    def errors(self) -> List[Dict[Any, Any]]:
        self._errors.sort(key=lambda e: e.line_num)
        return [error.dict() for error in self._errors]

    def create(self, project: Project, user):
        self.examples.save_label(project)
        ids = self.examples.save_data(project)
        self.examples.save_annotation(project, user, ids)
