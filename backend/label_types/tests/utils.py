from model_mommy import mommy

from projects.models import BOUNDING_BOX, SEGMENTATION


def make_label(project, **kwargs):
    if project.project_type.endswith("Classification") or project.project_type in {BOUNDING_BOX, SEGMENTATION}:
        return mommy.make("CategoryType", project=project, **kwargs)
    else:
        return mommy.make("SpanType", project=project, **kwargs)
