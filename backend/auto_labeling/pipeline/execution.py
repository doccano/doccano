import abc
from typing import List, Type

from auto_labeling_pipeline.labels import SequenceLabels, Seq2seqLabels, ClassificationLabels, Labels
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.pipeline import pipeline
from auto_labeling_pipeline.postprocessing import PostProcessor

from api.models import Example, Project, User
from api.models import CategoryType, SpanType
from api.models import Annotation, Category, Span, TextLabel


def get_label_collection(task_type: str) -> Type[Labels]:
    return {
        'Category': ClassificationLabels,
        'Span': SequenceLabels,
        'Text': Seq2seqLabels
    }[task_type]


class LabelCollection(abc.ABC):
    label_type = None
    model = None

    def __init__(self, labels):
        self.labels = labels

    def transform(self, project: Project, example: Example, user: User) -> List[Annotation]:
        mapping = {
            c.text: c for c in self.label_type.objects.filter(project=project)
        }
        annotations = []
        for label in self.labels:
            if label['label'] not in mapping:
                continue
            label['example'] = example
            label['label'] = mapping[label['label']]
            label['user'] = user
            annotations.append(self.model(**label))
        return annotations

    def save(self, project: Project, example: Example, user: User):
        labels = self.transform(project, example, user)
        labels = self.model.objects.filter_annotatable_labels(labels, project)
        self.model.objects.bulk_create(labels)


class Categories(LabelCollection):
    label_type = CategoryType
    model = Category


class Spans(LabelCollection):
    label_type = SpanType
    model = Span


class Texts(LabelCollection):
    model = TextLabel

    def transform(self, project: Project, example: Example, user: User) -> List[Annotation]:
        annotations = []
        for label in self.labels:
            label['example'] = example
            label['user'] = user
            annotations.append(self.model(**label))
        return annotations


def create_labels(task_type: str, labels: Labels) -> LabelCollection:
    return {
        'Category': Categories,
        'Span': Spans,
        'Text': Texts
    }[task_type](labels.dict())


def execute_pipeline(text: str,
                     task_type: str,
                     model_name: str,
                     model_attrs: dict,
                     template: str,
                     label_mapping: dict):
    label_collection = get_label_collection(task_type)
    model = RequestModelFactory.create(
        model_name=model_name,
        attributes=model_attrs
    )
    template = MappingTemplate(
        label_collection=label_collection,
        template=template
    )
    post_processor = PostProcessor(label_mapping)
    labels = pipeline(
        text=text,
        request_model=model,
        mapping_template=template,
        post_processing=post_processor
    )
    labels = create_labels(task_type, labels)
    return labels
