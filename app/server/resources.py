from import_export import resources
from .models import Project, Label, Document, DocumentAnnotation

class DocumentResource(resources.ModelResource):

    class Meta:
        model = Document

class DocumentAnnotationResource(resources.ModelResource):

    class Meta:
        model = DocumentAnnotation


class LabelResource(resources.ModelResource):

    class Meta:
        model = Label