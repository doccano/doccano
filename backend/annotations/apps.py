from django.apps import AppConfig

class AnnotationsConfig(AppConfig):
    name = 'annotations'

    def ready(self):
        import annotations.signals