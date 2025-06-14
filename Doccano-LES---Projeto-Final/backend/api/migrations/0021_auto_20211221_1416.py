from django.db import migrations


def copy_label_to_subclass(apps, schema_editor):
    Label = apps.get_model("api", "Label")
    for label in Label.objects.all():
        project_type = label.project.project_type
        if project_type.endswith("Classification"):
            model = apps.get_model("api", "CategoryType")
        else:
            model = apps.get_model("api", "SpanType")
        model.objects.create(
            id=label.id,
            text=label.text,
            prefix_key=label.prefix_key,
            suffix_key=label.suffix_key,
            project=label.project,
            background_color=label.background_color,
            text_color=label.text_color,
            created_at=label.created_at,
            updated_at=label.updated_at,
        )


def delete_subclass_object(apps, schema_editor):
    CategoryType = apps.get_model("api", "CategoryType")
    SpanType = apps.get_model("api", "SpanType")
    Label = apps.get_model("api", "Label")
    for model in [CategoryType, SpanType]:
        for label in model.objects.all():
            old_label = Label(
                id=label.id,
                text=label.text,
                prefix_key=label.prefix_key,
                suffix_key=label.suffix_key,
                project=label.project,
                background_color=label.background_color,
                text_color=label.text_color,
                created_at=label.created_at,
                updated_at=label.updated_at,
            )
            label.delete()
            old_label.save()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_auto_20211221_1415"),
    ]

    operations = [
        migrations.RunPython(code=copy_label_to_subclass, reverse_code=delete_subclass_object),
    ]
