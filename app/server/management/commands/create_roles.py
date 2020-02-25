from django.core.management.base import BaseCommand
from django.db import DatabaseError
from django.conf import settings

from api.models import Role, User
from api.permissions import add_superuser_to_all_projects


class Command(BaseCommand):
    help = 'Non-interactively create default roles'

    def handle(self, *args, **options):
        try:
            role_names = [
                settings.ROLE_PROJECT_ADMIN,
                settings.ROLE_ANNOTATOR,
                settings.ROLE_ANNOTATION_APPROVER,
                settings.ROLE_VIEWER,
            ]
        except KeyError as key_error:
            self.stderr.write(self.style.ERROR(f'Missing Key: "{key_error}"'))
            return

        for role_name in role_names:
            role = Role(name=role_name)
            try:
                role.save()
            except DatabaseError as db_error:
                self.stderr.write(self.style.ERROR(f'Database Error: "{db_error}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Role created successfully "{role_name}"'))

        add_superuser_to_all_projects(*list(User.objects.filter(is_superuser=True)))
