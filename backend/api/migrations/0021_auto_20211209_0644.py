from django.db import migrations


def update_label_type(apps, schema_editor):
    Label = apps.get_model('api', 'Label')
    for label in Label.objects.all():
        project_type = label.project.project_type
        if project_type.endswith('Classification'):
            label.task_type = 'Category'
        else:
            label.task_type = 'Span'
        label.save()


# def move_relation_type_to_label(apps, schema_editor):
#     Label = apps.get_model('api', 'Label')
#     RelationTypes = apps.get_model('api', 'RelationTypes')
#     for relation_type in RelationTypes.objects.all():
#         Label.objects.create(
#             text=relation_type.name,
#             project=relation_type.project,
#             background_color=relation_type.color,
#             task_type='Relation'
#         )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_label_task_type'),
    ]

    operations = [
        migrations.RunPython(update_label_type),
        # migrations.RunPython(move_relation_type_to_label),
    ]
