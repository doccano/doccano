# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_set_default_perspective_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perspective',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ] 