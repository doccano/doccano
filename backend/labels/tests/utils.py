from model_mommy import mommy

from projects.models import (
    DOCUMENT_CLASSIFICATION,
    SEQ2SEQ,
    SEQUENCE_LABELING,
    SPEECH2TEXT,
)


def make_annotation(task, doc, user, **kwargs):
    annotation_model = {
        DOCUMENT_CLASSIFICATION: "Category",
        SEQUENCE_LABELING: "Span",
        SEQ2SEQ: "TextLabel",
        SPEECH2TEXT: "TextLabel",
    }.get(task)
    return mommy.make(annotation_model, example=doc, user=user, **kwargs)
