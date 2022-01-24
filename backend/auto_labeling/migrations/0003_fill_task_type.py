from django.db import migrations


def fill_task_type(apps, schema_editor):
    AutoLabelingConfig = apps.get_model('auto_labeling', 'AutoLabelingConfig')
    for config in AutoLabelingConfig.objects.all():
        project = config.project
        config.task_type = project.project_type
        config.save()


class Migration(migrations.Migration):

    dependencies = [
        ('auto_labeling', '0002_autolabelingconfig_task_type'),
    ]

    operations = [
        migrations.RunPython(
            code=fill_task_type,
            reverse_code=migrations.RunPython.noop
        )
    ]
