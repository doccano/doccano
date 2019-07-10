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

    def test_sslmode_can_be_disabled_via_database_url(self):
        with setenv('DATABASE_URL', 'pgsql://u:p@h/d?sslmode=disable'):
            self._assert_sslmode_is('disable')

    def test_sslmode_can_be_required_via_database_url(self):
        with setenv('DATABASE_URL', 'pgsql://u:p@h/d?sslmode=require'):
            self._assert_sslmode_is('require')

    def test_database_url_with_complex_user(self):
        with setenv('DATABASE_URL', 'pgsql://user%40host:p@h/d'):
            self._assert_user_is('user@host')

    def _assert_sslmode_is(self, expected):
        actual = settings.DATABASES['default'].get('OPTIONS', {}).get('sslmode')
        self.assertEqual(actual, expected)

    def _assert_user_is(self, expected):
        actual = settings.DATABASES['default'].get('USER', '')
        self.assertEqual(actual, expected)


@contextmanager
def setenv(key, value):
    environ[key] = value
    reload(settings)
    yield
    del environ[key]

