from django.contrib import admin

from .models import Annotation, Label

admin.site.register(Annotation)
admin.site.register(Label)
