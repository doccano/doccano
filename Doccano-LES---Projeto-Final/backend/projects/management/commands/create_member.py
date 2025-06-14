from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from models import Project

from ...models import Member
from roles.models import Role


class Command(BaseCommand):
    help = "Non-interactively create a member"

    @classmethod
    def add_arguments(self, parser):
        parser.add_argument("--rolename", default=None, help="The name of the role.")
        parser.add_argument("--username", default=None, help="The name of the user.")
        parser.add_argument("--projectname", default=None, help="The name of the project.")

    def handle(self, *args, **options):
        rolename = options.get("rolename")
        username = options.get("username")
        projectname = options.get("projectname")

        if not rolename or not username or not projectname:
            raise CommandError("--rolename  --projectname  --username are required for the member")

        if rolename and projectname and username:
            try:
                role = Role.objects.get(name=rolename)
                user = User.objects.get(username=username)
                project = Project.objects.get(name=projectname)
                member = Member.objects.create(role_id=role.id, user_id=user.id, project_id=project.id)
            except Exception as ex:
                self.stderr.write(self.style.ERROR('Error occurred while creating member "%s"' % ex))
            else:
                self.stdout.write(self.style.SUCCESS('Member created successfully "%s"' % member.id))
