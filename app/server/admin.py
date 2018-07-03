from django.contrib import admin

from .models import Annotation, Label, Document, Project

admin.site.register(Annotation)
admin.site.register(Label)
admin.site.register(Document)
admin.site.register(Project)
