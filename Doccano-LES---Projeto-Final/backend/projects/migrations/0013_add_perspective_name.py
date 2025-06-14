# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_update_question_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='perspective',
            name='name',
            field=models.CharField(default='Default Perspective', max_length=100),
            preserve_default=False,
        ),
    ] 