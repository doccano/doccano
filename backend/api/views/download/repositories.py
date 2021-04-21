import abc
import itertools
from collections import defaultdict
from typing import Dict, Iterator, List

from ...models import Project
from .data import Record


class BaseRepository(abc.ABC):

    def __init__(self, project: Project):
        self.project = project

    @abc.abstractmethod
    def list(self, export_approved=False) -> Iterator[Record]:
        pass


class TextRepository(BaseRepository):

    @property
    def docs(self):
        return self.project.documents.all()

    def list(self, export_approved=False):
        docs = self.docs
        if export_approved:
            docs = docs.exclude(annotations_approved_by=None)

        for doc in docs:
            label_per_user = self.label_per_user(doc)
            if self.project.collaborative_annotation:
                label_per_user = self.reduce_user(label_per_user)
            for user, label in label_per_user.items():
                yield Record(
                    id=doc.id,
                    data=doc.text,
                    label=label,
                    user=user,
                    metadata=doc.meta
                )
            # todo:
            # If there is no label, export the doc with `unknown` user.
            # This is a quick solution.
            # In the future, the doc without label will be exported
            # with the user who approved the doc.
            # This means I will allow each user to be able to approve the doc.
            if len(label_per_user) == 0:
                yield Record(
                    id=doc.id,
                    data=doc.text,
                    label=[],
                    user='unknown',
                    metadata={}
                )

    @abc.abstractmethod
    def label_per_user(self, doc) -> Dict:
        raise NotImplementedError()

    def reduce_user(self, label_per_user: Dict[str, List]):
        value = list(itertools.chain(*label_per_user.values()))
        return {'all': value}


class TextClassificationRepository(TextRepository):

    @property
    def docs(self):
        return self.project.documents.prefetch_related(
            'doc_annotations__user', 'doc_annotations__label'
        )

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.doc_annotations.all():
            label_per_user[a.user.username].append(a.label.text)
        return label_per_user


class SequenceLabelingRepository(TextRepository):

    @property
    def docs(self):
        return self.project.documents.prefetch_related(
            'seq_annotations__user', 'seq_annotations__label'
        )

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.seq_annotations.all():
            label = (a.start_offset, a.end_offset, a.label.text)
            label_per_user[a.user.username].append(label)
        return label_per_user


class Seq2seqRepository(TextRepository):

    @property
    def docs(self):
        return self.project.documents.prefetch_related(
            'seq2seq_annotations__user'
        )

    def label_per_user(self, doc) -> Dict:
        label_per_user = defaultdict(list)
        for a in doc.seq2seq_annotations.all():
            label_per_user[a.user.username].append(a.text)
        return label_per_user
