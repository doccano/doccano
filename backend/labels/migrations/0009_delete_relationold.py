# Generated by Django 4.0.2 on 2022-02-22 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0008_auto_20220222_0630"),
    ]

    operations = [
        migrations.DeleteModel(
            name="RelationOld",
        ),
    ]