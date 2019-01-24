import sys
import time

from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Blocks until the database is available'

    def add_arguments(self, parser):
        parser.add_argument('--poll_seconds', type=float, default=3)
        parser.add_argument('--max_retries', type=int, default=60)

    def handle(self, *args, **options):
        max_retries = options['max_retries']
        poll_seconds = options['poll_seconds']

        for retry in range(max_retries):
            try:
                connection.ensure_connection()
            except OperationalError as ex:
                self.stdout.write(
                    'Database unavailable on attempt {attempt}/{max_retries}:'
                    ' {error}'.format(
                        attempt=retry + 1,
                        max_retries=max_retries,
                        error=ex))
                time.sleep(poll_seconds)
            else:
                break
        else:
            self.stdout.write(self.style.ERROR('Database unavailable'))
            sys.exit(1)
