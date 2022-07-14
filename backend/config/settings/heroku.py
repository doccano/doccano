import django_heroku

from .base import *  # noqa: F401,F403

django_heroku.settings(locals(), test_runner=False, staticfiles=False)
