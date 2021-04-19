import abc
from collections import defaultdict
from typing import Dict, Iterator

from ...models import Project
from .data import Record


class BaseRepository(abc.ABC):

    def __init__(self, project: Project):
        self.project = project

    @abc.abstractmethod
    def list(self, export_approved=False) -> Iterator[Record]:
        pass


class TextRepository(BaseRepository):

    def list(self, export_approved=False):
        docs = self.project.documents.all()
        if export_approved:
            docs = docs.exclude(annotations_approved_by=None)

        for doc in docs:
            label_per_user = self.label_per_user(doc)
            for user, label in label_per_user.items():
                yield Record(
                    id=doc.id,
                    data=doc.text,
                    label=label,
                    user=user,
                    metadata=doc.meta
                )

    @abc.abstractmethod
    def label_per_user(self, doc) -> Dict:
        raise NotImplementedError()


class TextClassificationRepository(TextRepository):

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.doc_annotations.all():
            label_per_user[a.user.username].append(a.label.text)
        return label_per_user


class SequenceLabelingRepository(TextRepository):

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.seq_annotations.all():
            label = (a.start_offset, a.end_offset, a.label.text)
            label_per_user[a.user.username].append(label)
        return label_per_user


class Seq2seqRepository(TextRepository):

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.seq2seq_annotations.all():
            label_per_user[a.user.username].append(a.text)
        return label_per_user
