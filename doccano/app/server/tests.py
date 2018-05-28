from django.test import TestCase

from .models import Project


class ProjectModelTest(TestCase):

    def test_string_representation(self):
        project = Project(name='my project', description='my description')
        self.assertEqual(str(project), project.name)
