import sys

sys.path.append('../api')

from api.models import Project
from django import forms


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'project_type', 'users', 'randomize_document_order')
