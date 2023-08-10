from model_mommy import mommy


def make_comment(doc, user):
    return mommy.make("Comment", example=doc, user=user)


def make_doc(project):
    return mommy.make("Example", text="example", project=project)


def make_image(project, filepath):
    return mommy.make("Example", filename=filepath, project=project)


def make_example_state(example, user):
    return mommy.make("ExampleState", example=example, confirmed_by=user)


def make_assignment(project, example, user):
    return mommy.make("Assignment", project=project, example=example, assignee=user)
