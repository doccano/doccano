from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = "Non-interactively create an admin user"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--password", default=None, help="The password for the admin.")

    def handle(self, *args, **options):
        password = options.get("password")
        username = options.get("username")

        if not username:
            self.stderr.write("Error: Blank username isn't allowed.")
            raise CommandError("--username is required if specifying --password")

        if not password:
            self.stderr.write("Error: Blank password isn't allowed.")
            raise CommandError("--password is required")

        if password == "password":
            self.stdout.write(self.style.WARNING("Warning: You should change the default password."))

        try:
            super().handle(*args, **options)
        except Exception as err:
            if "is already taken" in str(err):
                self.stderr.write(f"User {username} already exists.")
            else:
                raise

        database = options.get("database")
        db = self.UserModel._default_manager.db_manager(database)
        user = db.get(username=username)
        user.set_password(password)
        message = f"Setting password for User {username}."
        self.stdout.write(self.style.SUCCESS(message))
        user.save()
