from typing import Type

from auto_labeling_pipeline.labels import SequenceLabels, Seq2seqLabels, ClassificationLabels, Labels
from auto_labeling_pipeline.mappings import MappingTemplate
from auto_labeling_pipeline.models import RequestModelFactory
from auto_labeling_pipeline.pipeline import pipeline
from auto_labeling_pipeline.postprocessing import PostProcessor


def get_label_collection(task_type: str) -> Type[Labels]:
    return {
        'Category': ClassificationLabels,
        'Span': SequenceLabels,
        'Text': Seq2seqLabels
    }[task_type]


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
    return labels.dict()
