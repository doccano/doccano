# Generated manually

from django.db import migrations


def set_default_perspective_names(apps, schema_editor):
    Perspective = apps.get_model('projects', 'Perspective')
    
    for perspective in Perspective.objects.filter(name__isnull=True):
        # Define um nome padrão baseado no ID do projeto
        perspective.name = f"Perspectiva do Projeto {perspective.project.id}"
        perspective.save()


def reverse_set_default_perspective_names(apps, schema_editor):
    # Não é necessário reverter esta operação
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_add_perspective_name'),
    ]

    operations = [
        migrations.RunPython(
            set_default_perspective_names,
            reverse_set_default_perspective_names,
        ),
    ] 