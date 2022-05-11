import itertools
from collections import defaultdict
from typing import List, Type

from .readers import BaseReader, Record
from examples.models import Example
from label_types.models import CategoryType, LabelType, SpanType
from projects.models import Project


def group_by_class(instances):
    groups = defaultdict(list)
    for instance in instances:
        groups[instance.__class__].append(instance)
    return groups


class Writer:
    def __init__(self, batch_size: int):
        self.batch_size = batch_size

    def save(self, reader: BaseReader, project: Project, user):
        for batch in reader.batch(self.batch_size):
            self.create(project, user, batch)

    def create(self, project: Project, user, batch: List[Record]):
        self.save_label_type(project, batch)
        ids = self.save_example(project, batch)
        self.save_label(project, user, ids, batch)

    def save_label_type(self, project: Project, batch: List[Record]):
        labels = list(itertools.chain.from_iterable([example.create_label(project) for example in batch]))
        labels = list(filter(None, labels))
        groups = group_by_class(labels)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances, ignore_conflicts=True)

    def save_example(self, project: Project, batch: List[Record]) -> List[Example]:
        examples = [example.create_data(project) for example in batch]
        return Example.objects.bulk_create(examples)

    def save_label(self, project: Project, user, examples, batch: List[Record]):
        mapping = {}
        label_types: List[Type[LabelType]] = [CategoryType, SpanType]
        for model in label_types:
            for label in model.objects.filter(project=project):
                mapping[label.text] = label

        annotations = list(
            itertools.chain.from_iterable(
                [data.create_annotation(user, example, mapping) for data, example in zip(batch, examples)]
            )
        )
        groups = group_by_class(annotations)
        for klass, instances in groups.items():
            klass.objects.bulk_create(instances)
