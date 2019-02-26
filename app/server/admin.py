from django.contrib import admin

from .models import Label, Document, Project
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation
from .resources import DocumentResource, DocumentAnnotationResource
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

class DocumentAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = DocumentResource

class DocumentAnnotationAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = DocumentAnnotationResource

admin.site.register(DocumentAnnotation, DocumentAnnotationAdmin)
admin.site.register(SequenceAnnotation)
admin.site.register(Seq2seqAnnotation)
admin.site.register(Label)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Project)



