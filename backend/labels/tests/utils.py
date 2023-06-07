from model_mommy import mommy

from projects.models import ProjectType


def make_annotation(task, doc, user, **kwargs):
    annotation_model = {
        ProjectType.DOCUMENT_CLASSIFICATION: "Category",
        ProjectType.SEQUENCE_LABELING: "Span",
        ProjectType.SEQ2SEQ: "TextLabel",
        ProjectType.SPEECH2TEXT: "TextLabel",
    }.get(task)
    return mommy.make(annotation_model, example=doc, user=user, **kwargs)
