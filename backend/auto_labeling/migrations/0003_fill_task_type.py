from django.db import migrations

from projects.models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ, SPEECH2TEXT, IMAGE_CLASSIFICATION


def fill_task_type(apps, schema_editor):
    AutoLabelingConfig = apps.get_model("auto_labeling", "AutoLabelingConfig")
    for config in AutoLabelingConfig.objects.all():
        project = config.project
        if project.project_type in [DOCUMENT_CLASSIFICATION, IMAGE_CLASSIFICATION]:
            config.task_type = "Category"
        elif project.project_type in [SEQ2SEQ, SPEECH2TEXT]:
            config.task_type = "Text"
        elif project.project_type in [SEQUENCE_LABELING]:
            config.task_type = "Span"
        else:
            config.task_type = "Category"
        config.save()


class Migration(migrations.Migration):

    dependencies = [
        ("auto_labeling", "0002_autolabelingconfig_task_type"),
    ]

    operations = [migrations.RunPython(code=fill_task_type, reverse_code=migrations.RunPython.noop)]
