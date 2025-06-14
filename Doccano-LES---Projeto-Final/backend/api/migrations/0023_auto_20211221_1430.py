from django.db import migrations


def copy_annotation(apps, schema_editor):
    Category = apps.get_model("api", "Category")
    Span = apps.get_model("api", "Span")
    for model in [Category, Span]:
        for annotation in model.objects.all():
            if model == Category:
                LabelModel = apps.get_model("api", "CategoryType")
            else:
                LabelModel = apps.get_model("api", "SpanType")
            label = LabelModel.objects.get(pk=annotation.label.id)
            annotation.new_label = label
            annotation.save()


def delete_annotation(apps, schema_editor):
    Category = apps.get_model("api", "Category")
    Span = apps.get_model("api", "Span")
    for model in [Category, Span]:
        for annotation in model.objects.all():
            annotation.new_label = None
            annotation.save()


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0022_auto_20211221_1430"),
    ]

    operations = [
        migrations.RunPython(code=copy_annotation, reverse_code=delete_annotation),
    ]
