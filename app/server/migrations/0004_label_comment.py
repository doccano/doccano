# Generated by Django 2.1.5 on 2019-02-13 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_shortcut'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='comment',
            field=models.CharField(default='', max_length=2000),
        ),
    ]
