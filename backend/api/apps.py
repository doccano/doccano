import importlib

from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = 'Api'

    def ready(self):
        importlib.import_module('api.signals')
