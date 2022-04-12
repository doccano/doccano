import os

from django.db import migrations


def store_filename(apps, schema_editor):
    Example = apps.get_model("examples", "Example")
    for example in Example.objects.all():
        example.upload_name = os.path.basename(example.filename.name)
        example.save()


class Migration(migrations.Migration):

    dependencies = [
        ("examples", "0004_example_upload_name"),
    ]

    operations = [migrations.RunPython(code=store_filename, reverse_code=migrations.RunPython.noop)]
