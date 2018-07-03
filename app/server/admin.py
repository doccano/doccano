from django.contrib import admin

from .models import Label, Document, Project
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation

admin.site.register(DocumentAnnotation)
admin.site.register(SequenceAnnotation)
admin.site.register(Seq2seqAnnotation)
admin.site.register(Label)
admin.site.register(Document)
admin.site.register(Project)
