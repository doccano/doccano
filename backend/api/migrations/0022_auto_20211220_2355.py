from django.db import migrations


def copy_label_to_subclass(apps, schema_editor):
    Label = apps.get_model('api', 'Label')
    for label in Label.objects.all():
        project_type = label.project.project_type
        if project_type.endswith('Classification'):
            model = apps.get_model('api', 'DocType')
            annotation_model = apps.get_model('api', 'Category')
        else:
            model = apps.get_model('api', 'SpanType')
            annotation_model = apps.get_model('api', 'Span')
        new_label = model.objects.create(
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
        for el in annotation_model.objects.filter(label=label):
            el.label_new = new_label
            el.save()


def delete_subclass_object(apps, schema_editor):
    DocType = apps.get_model('api', 'DocType')
    SpanType = apps.get_model('api', 'SpanType')
    Label = apps.get_model('api', 'Label')
    for model in [DocType, SpanType]:
        for label in model.objects.all():
            project_type = label.project.project_type
            old_label = Label(
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
            if project_type.endswith('Classification'):
                annotation_model = apps.get_model('api', 'Category')
            else:
                annotation_model = apps.get_model('api', 'Span')
            elements = [el for el in annotation_model.objects.filter(label_id=label.id)]
            label.delete()
            old_label.save()
            for el in elements:
                el.label = old_label
                el.label_new = None
                el.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20211221_0553'),
    ]

    operations = [
        migrations.RunPython(
            code=copy_label_to_subclass,
            reverse_code=delete_subclass_object
        ),
    ]
