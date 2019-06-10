from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'project_type', 'users', 'randomize_document_order')
