from model_mommy import mommy


def make_label(project, **kwargs):
    if project.project_type.endswith("Classification"):
        return mommy.make("CategoryType", project=project, **kwargs)
    else:
        return mommy.make("SpanType", project=project, **kwargs)
