import abc
import itertools
from collections import defaultdict
from typing import Dict, Iterator, List, Tuple, Union

from .data import Record
from examples.models import Example
from projects.models import Project

SpanType = Tuple[int, int, str]


class BaseRepository(abc.ABC):
    def __init__(self, project: Project):
        self.project = project

    @abc.abstractmethod
    def list(self, export_approved=False) -> Iterator[Record]:
        pass


class FileRepository(BaseRepository):
    def list(self, export_approved=False) -> Iterator[Record]:
        examples = self.project.examples.all()
        if export_approved:
            examples = examples.exclude(annotations_approved_by=None)

        for example in examples:
            label_per_user = self.label_per_user(example)
            if self.project.collaborative_annotation:
                label_per_user = self.reduce_user(label_per_user)
            for user, label in label_per_user.items():
                yield Record(
                    data_id=example.id,
                    data=str(example.filename).split("/")[-1],
                    label=label,
                    user=user,
                    metadata=example.meta,
                )
            # todo:
            # If there is no label, export the doc with `unknown` user.
            # This is a quick solution.
            # In the future, the doc without label will be exported
            # with the user who approved the doc.
            # This means I will allow each user to be able to approve the doc.
            if len(label_per_user) == 0:
                yield Record(
                    data_id=example.id, data=str(example.filename).split("/")[-1], label=[], user="unknown", metadata={}
                )

    def label_per_user(self, example) -> Dict:
        label_per_user = defaultdict(list)
        for a in example.categories.all():
            label_per_user[a.user.username].append(a.label.text)
        return label_per_user

    def reduce_user(self, label_per_user: Dict[str, List]):
        value = list(itertools.chain(*label_per_user.values()))
        return {"all": value}


class Speech2TextRepository(FileRepository):
    def label_per_user(self, example) -> Dict:
        label_per_user = defaultdict(list)
        for a in example.texts.all():
            label_per_user[a.user.username].append(a.text)
        return label_per_user


class TextRepository(BaseRepository):
    @property
    def docs(self):
        return Example.objects.filter(project=self.project)

    def list(self, export_approved=False):
        docs = self.docs
        if export_approved:
            docs = docs.exclude(annotations_approved_by=None)

        for doc in docs:
            label_per_user = self.label_per_user(doc)
            if self.project.collaborative_annotation:
                label_per_user = self.reduce_user(label_per_user)
            for user, label in label_per_user.items():
                yield Record(data_id=doc.id, data=doc.text, label=label, user=user, metadata=doc.meta)
            # todo:
            # If there is no label, export the doc with `unknown` user.
            # This is a quick solution.
            # In the future, the doc without label will be exported
            # with the user who approved the doc.
            # This means I will allow each user to be able to approve the doc.
            if len(label_per_user) == 0:
                yield Record(data_id=doc.id, data=doc.text, label=[], user="unknown", metadata={})

    @abc.abstractmethod
    def label_per_user(self, doc) -> Dict:
        raise NotImplementedError()

    def reduce_user(self, label_per_user: Dict[str, List]):
        value = list(itertools.chain(*label_per_user.values()))
        return {"all": value}


class TextClassificationRepository(TextRepository):
    @property
    def docs(self):
        return Example.objects.filter(project=self.project).prefetch_related("categories__user", "categories__label")

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.categories.all():
            label_per_user[a.user.username].append(a.label.text)
        return label_per_user


class SequenceLabelingRepository(TextRepository):
    @property
    def docs(self):
        return Example.objects.filter(project=self.project).prefetch_related("spans__user", "spans__label")

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.spans.all():
            label = (a.start_offset, a.end_offset, a.label.text)
            label_per_user[a.user.username].append(label)
        return label_per_user


class RelationExtractionRepository(TextRepository):
    @property
    def docs(self):
        return Example.objects.filter(project=self.project).prefetch_related(
            "spans__user", "spans__label", "relations__user", "relations__type"
        )

    def label_per_user(self, doc) -> Dict:
        relation_per_user: Dict = defaultdict(list)
        span_per_user: Dict = defaultdict(list)
        label_per_user: Dict = defaultdict(dict)
        for relation in doc.relations.all():
            relation_per_user[relation.user.username].append(
                {
                    "id": relation.id,
                    "from_id": relation.from_id.id,
                    "to_id": relation.to_id.id,
                    "type": relation.type.text,
                }
            )
        for span in doc.spans.all():
            span_per_user[span.user.username].append(
                {
                    "id": span.id,
                    "start_offset": span.start_offset,
                    "end_offset": span.end_offset,
                    "label": span.label.text,
                }
            )
        for user, relations in relation_per_user.items():
            label_per_user[user]["relations"] = relations
        for user, span in span_per_user.items():
            label_per_user[user]["entities"] = span
        return label_per_user


class Seq2seqRepository(TextRepository):
    @property
    def docs(self):
        return Example.objects.filter(project=self.project).prefetch_related("texts__user")

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.texts.all():
            label_per_user[a.user.username].append(a.text)
        return label_per_user


class IntentDetectionSlotFillingRepository(TextRepository):
    @property
    def docs(self):
        return Example.objects.filter(project=self.project).prefetch_related(
            "categories__user", "categories__label", "spans__user", "spans__label"
        )

    def label_per_user(self, doc) -> Dict:
        category_per_user: Dict[str, List[str]] = defaultdict(list)
        span_per_user: Dict[str, List[SpanType]] = defaultdict(list)
        label_per_user: Dict[str, Dict[str, Union[List[str], List[SpanType]]]] = defaultdict(dict)
        for a in doc.categories.all():
            category_per_user[a.user.username].append(a.label.text)
        for a in doc.spans.all():
            span_per_user[a.user.username].append((a.start_offset, a.end_offset, a.label.text))
        for user, cats in category_per_user.items():
            label_per_user[user]["cats"] = cats
        for user, span in span_per_user.items():
            label_per_user[user]["entities"] = span
        return label_per_user
