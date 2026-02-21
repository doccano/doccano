# Generated to fix MySQL compatibility: TEXT columns cannot be used in
# unique key specifications without a key length (MySQL error 1170).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0016_segmentation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="textlabel",
            name="text",
            field=models.CharField(max_length=500),
        ),
    ]
