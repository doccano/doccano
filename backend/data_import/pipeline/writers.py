import itertools
from collections import defaultdict
from typing import List, Type

from django.conf import settings

from .readers import BaseReader, Record
from examples.models import Example
from label_types.models import CategoryType, LabelType, SpanType
from projects.models import Project


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

    def __getitem__(self, item):
        return self.buffer[item]

    def add(self, data):
        self.buffer.append(data)

    def clear(self):
        self.buffer = []

    def is_full(self):
        return len(self) >= self.buffer_size

    def is_empty(self):
        return len(self) == 0


class Writer:
    def __init__(self, batch_size: int):
        self.examples = Examples(batch_size)

    def save(self, reader: BaseReader, project: Project, user):
        it = iter(reader)
        while True:
            try:
                example = next(it)
            except StopIteration:
                break

            self.examples.add(example)
            if self.examples.is_full():
                self.create(project, user)
                self.examples.clear()
        if not self.examples.is_empty():
            self.create(project, user)
            self.examples.clear()

    def create(self, project: Project, user):
        self.save_label_type(project)
        ids = self.save_example(project)
        self.save_label(project, user, ids)

    def save_label_type(self, project: Project):
        labels = list(itertools.chain.from_iterable([example.create_label(project) for example in self.examples]))
        labels = list(filter(None, labels))
        groups = group_by_class(labels)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances, ignore_conflicts=True)

    def save_example(self, project: Project) -> List[Example]:
        examples = [example.create_data(project) for example in self.examples]
        return Example.objects.bulk_create(examples)

    def save_label(self, project: Project, user, examples):
        mapping = {}
        label_types: List[Type[LabelType]] = [CategoryType, SpanType]
        for model in label_types:
            for label in model.objects.filter(project=project):
                mapping[label.text] = label

        annotations = list(
            itertools.chain.from_iterable(
                [data.create_annotation(user, example, mapping) for data, example in zip(self.examples, examples)]
            )
        )
        groups = group_by_class(annotations)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances)
