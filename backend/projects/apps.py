import importlib

from django.apps import AppConfig
from django.db.models.signals import post_save


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

    def ready(self):
        importlib.import_module('projects.signals')
        from api.models import Project
        from .signals import add_administrator_on_project_creation

        # Registering signals with the subclasses of project.
        for project in Project.__subclasses__():
            post_save.connect(add_administrator_on_project_creation, project)
