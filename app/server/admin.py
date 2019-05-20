from django.contrib import admin

from .models import Label, Document, Project
from .models import DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation
from .resources import DocumentResource, DocumentAnnotationResource
from import_export.admin import ImportExportModelAdmin, ImportExportMixin


class DocumentAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = DocumentResource
    model = Document
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        for o in obj.all():
            o.delete()
    delete_model.short_description = 'Delete selected Docs'


class DocumentAnnotationAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = DocumentAnnotationResource


admin.site.register(DocumentAnnotation, DocumentAnnotationAdmin)
admin.site.register(SequenceAnnotation)
admin.site.register(Seq2seqAnnotation)
admin.site.register(Label)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Project)
