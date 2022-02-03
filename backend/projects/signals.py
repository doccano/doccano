from django.conf import settings

from api.models import Project
from roles.models import Role
from .models import Member


def add_administrator_on_project_creation(sender, instance: Project, created: bool, **kwargs):
    # In the case of creating a project.
    if created:
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        Member.objects.create(
            project=instance,
            user=instance.created_by,
            role=admin_role,
        )
