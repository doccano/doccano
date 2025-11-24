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

    # For CustomRESTRequestModel, ensure body has default value if empty
    model_attrs = config.model_attrs.copy()
    if config.model_name == "Custom REST Request":
        if "params" not in model_attrs or not isinstance(model_attrs.get("params"), dict):
            model_attrs["params"] = {}
        if "headers" not in model_attrs or not isinstance(model_attrs.get("headers"), dict):
            model_attrs["headers"] = {}
        # Ensure Content-Type header is set for JSON requests
        if "Content-Type" not in model_attrs["headers"]:
            model_attrs["headers"]["Content-Type"] = "application/json"
        if "body" not in model_attrs or not isinstance(model_attrs.get("body"), dict) or not model_attrs.get("body"):
            # Set default body with text field
            model_attrs["body"] = {"text": "{{text}}"}

    model = RequestModelFactory.create(model_name=config.model_name, attributes=model_attrs)
    template = MappingTemplate(label_collection=label_collection, template=config.template)
    post_processor = PostProcessor(config.label_mapping)

    # For CustomRESTRequestModel, set the actual text in body (not template variable)
    # This is the same approach as views.py:119-123
    if config.model_name == "Custom REST Request" and hasattr(model, 'body') and isinstance(model.body, dict):
        import copy
        model = copy.deepcopy(model)
        model.body = {"text": data}

    labels = pipeline(text=data, request_model=model, mapping_template=template, post_processing=post_processor)
    labels = create_labels(config.task_type, labels)
    return labels
