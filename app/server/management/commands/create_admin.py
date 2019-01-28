from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Non-interactively create an admin user'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--password', default=None,
                            help='The password for the admin.')

    def handle(self, *args, **options):
        password = options.get('password')
        username = options.get('username')

        if password and not username:
            raise CommandError('--username is required if specifying --password')

        super(Command, self).handle(*args, **options)

        if password:
            database = options.get('database')
            db = self.UserModel._default_manager.db_manager(database)
            user = db.get(username=username)
            user.set_password(password)
            user.save()
