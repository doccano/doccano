from django.db import migrations

from projects.models import ProjectType


def fill_task_type(apps, schema_editor):
    AutoLabelingConfig = apps.get_model("auto_labeling", "AutoLabelingConfig")
    for config in AutoLabelingConfig.objects.all():
        project = config.project
        if project.project_type in [ProjectType.DOCUMENT_CLASSIFICATION, ProjectType.IMAGE_CLASSIFICATION]:
            config.task_type = "Category"
        elif project.project_type in [ProjectType.SEQ2SEQ, ProjectType.SPEECH2TEXT]:
            config.task_type = "Text"
        elif project.project_type in [ProjectType.SEQUENCE_LABELING]:
            config.task_type = "Span"
        else:
            config.task_type = "Category"
        config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("auto_labeling", "0002_autolabelingconfig_task_type"),
    ]

    operations = [migrations.RunPython(code=fill_task_type, reverse_code=migrations.RunPython.noop)]
