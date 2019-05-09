from contextlib import contextmanager
from importlib import reload
from os import environ

from django.test import TestCase

from app import settings


class TestDatabaseUrl(TestCase):
    def test_sslmode_defaults_to_required(self):
        with setenv('DATABASE_URL', 'pgsql://u:p@h/d'):
            self._assert_sslmode_is('require')

    def test_sslmode_not_set_for_sqlite(self):
        with setenv('DATABASE_URL', 'sqlite:///some/path'):
            self._assert_sslmode_is(None)

    def test_sslmode_can_be_set_via_database_url(self):
        with setenv('DATABASE_URL', 'pgsql://u:p@h/d?sslmode=disabled'):
            self._assert_sslmode_is('disabled')

    def _assert_sslmode_is(self, expected):
        reload(settings)
        actual = settings.DATABASES['default'].get('OPTIONS', {}).get('sslmode')
        self.assertEqual(actual, expected)


@contextmanager
def setenv(key, value):
    environ[key] = value
    yield
    del environ[key]

