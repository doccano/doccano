from django.contrib import admin

from .models import Annotation, Label, RawData

admin.site.register(Annotation)
admin.site.register(Label)
admin.site.register(RawData)
