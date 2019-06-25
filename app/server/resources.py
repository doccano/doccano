from import_export import resources
from .models import Project, Label, Document, DocumentAnnotation, DocumentMLMAnnotation

class DocumentResource(resources.ModelResource):

    class Meta:
        model = Document

class DocumentAnnotationResource(resources.ModelResource):

    class Meta:
        model = DocumentAnnotation

class DocumentMLMAnnotationResource(resources.ModelResource):

    class Meta:
        model = DocumentMLMAnnotation


class LabelResource(resources.ModelResource):

    class Meta:
        model = Label