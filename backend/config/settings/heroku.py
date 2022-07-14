import django_heroku

from .base import *  # noqa: F401,F403

django_heroku.settings(locals(), test_runner=False)
ALLOWED_HOSTS = ['.herokuapp.com']
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}
