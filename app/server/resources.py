from import_export import resources
from .models import Project, Label, Document, DocumentAnnotation, DocumentMLMAnnotation, Project
from django.contrib.auth.models import User

class DocumentResource(resources.ModelResource):

    class Meta:
        model = Document

class ProjectResource(resources.ModelResource):

    class Meta:
        model = Project

class DocumentAnnotationResource(resources.ModelResource):

    class Meta:
        model = DocumentAnnotation

class DocumentMLMAnnotationResource(resources.ModelResource):

    class Meta:
        model = DocumentMLMAnnotation

class UserResource(resources.ModelResource):

    class Meta:
        model = User


class LabelResource(resources.ModelResource):

    class Meta:
        model = Label