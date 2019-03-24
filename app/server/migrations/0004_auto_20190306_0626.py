# Generated by Django 2.1.5 on 2019-03-06 06:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('server', '0003_shortcut'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seq2seqProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Project')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('server.project',),
        ),
        migrations.CreateModel(
            name='Speech2textProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Project')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('server.project',),
        ),
        migrations.CreateModel(
            name='SequenceLabelingProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Project')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('server.project',),
        ),
        migrations.CreateModel(
            name='TextClassificationProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Project')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('server.project',),
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AddField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='documentannotation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentannotation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='label',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='label',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='project',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_server.project_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='seq2seqannotation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speech2textannotation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seq2seqannotation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='speech2textannotation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sequenceannotation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sequenceannotation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='project',
            name='guideline',
            field=models.TextField(default=''),
        ),
    ]
