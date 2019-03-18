from django.contrib import admin

from .models import Label, Document, Project
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation
from .models import TextClassificationProject, SequenceLabelingProject, Seq2seqProject

admin.site.register(DocumentAnnotation)
admin.site.register(SequenceAnnotation)
admin.site.register(Seq2seqAnnotation)
admin.site.register(Label)
admin.site.register(Document)
admin.site.register(Project)
admin.site.register(TextClassificationProject)
admin.site.register(SequenceLabelingProject)
admin.site.register(Seq2seqProject)
