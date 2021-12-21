from django.db import migrations


def assign_label_to_subclass(apps, schema_editor):
    Label = apps.get_model('api', 'Label')
    DocType = apps.get_model('api', 'DocType')
    SpanType = apps.get_model('api', 'SpanType')
    for label in Label.objects.all():
        project_type = label.project.project_type
        if project_type.endswith('Classification'):
            model = DocType
        else:
            model = SpanType
        label.delete()
        model(
            id=label.id,
            text=label.text,
            prefix_key=label.prefix_key,
            suffix_key=label.suffix_key,
            project=label.project,
            background_color=label.background_color,
            text_color=label.text_color,
            created_at=label.created_at,
            updated_at=label.updated_at
        ).save()


def assign_subclass_to_label(apps, schema_editor):
    Label = apps.get_model('api', 'Label')
    DocType = apps.get_model('api', 'DocType')
    SpanType = apps.get_model('api', 'SpanType')
    for model in [DocType, SpanType]:
        for label in model.objects.all():
            new_label = Label(
                id=label.id,
                text=label.text,
                prefix_key=label.prefix_key,
                suffix_key=label.suffix_key,
                project=label.project,
                background_color=label.background_color,
                text_color=label.text_color,
                created_at=label.created_at,
                updated_at=label.updated_at
            )
            label.delete()
            new_label.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20211220_2327'),
    ]

    operations = [
        migrations.RunPython(
            code=assign_label_to_subclass,
            reverse_code=assign_subclass_to_label
        ),
    ]
