# Generated manually - No-op migration for data_type field
# This migration assumes the data_type field already exists in the database

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_merge_20250614_2110'),
    ]

    operations = [
        # No operations - the field already exists in the database
        # This migration just records that the field should be considered as added
    ] 