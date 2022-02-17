from typing import Type

from auto_labeling_pipeline.labels import (
    ClassificationLabels,
    Labels,
    Seq2seqLabels,
    SequenceLabels,
)
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.pipeline import pipeline
from auto_labeling_pipeline.postprocessing import PostProcessor

from .labels import create_labels
from auto_labeling.models import AutoLabelingConfig


def get_label_collection(task_type: str) -> Type[Labels]:
    return {"Category": ClassificationLabels, "Span": SequenceLabels, "Text": Seq2seqLabels}[task_type]


def execute_pipeline(data: str, config: AutoLabelingConfig):
    label_collection = get_label_collection(config.task_type)
    model = RequestModelFactory.create(model_name=config.model_name, attributes=config.model_attrs)
    template = MappingTemplate(label_collection=label_collection, template=config.template)
    post_processor = PostProcessor(config.label_mapping)
    labels = pipeline(text=data, request_model=model, mapping_template=template, post_processing=post_processor)
    labels = create_labels(config.task_type, labels)
    return labels
