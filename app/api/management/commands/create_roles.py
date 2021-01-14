from api.models import Role
from django.core.management.base import BaseCommand
from django.db import DatabaseError
from django.conf import settings


class Command(BaseCommand):
    help = 'Non-interactively create default roles'

    def handle(self, *args, **options):
        try:
            role_names = [settings.ROLE_PROJECT_ADMIN, settings.ROLE_ANNOTATOR, settings.ROLE_ANNOTATION_APPROVER]
        except KeyError as key_error:
            self.stderr.write(self.style.ERROR(f'Missing Key: "{key_error}"'))
        for role_name in role_names:
            if Role.objects.filter(name=role_name).exists():
                continue
            role = Role()
            role.name = role_name
            try:
                role.save()
            except DatabaseError as db_error:
                self.stderr.write(self.style.ERROR(f'Database Error: "{db_error}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Role created successfully "{role_name}"'))
