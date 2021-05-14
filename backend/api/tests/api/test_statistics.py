from django.conf import settings
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import DOCUMENT_CLASSIFICATION, Example
from .utils import (TestUtilsMixin, assign_user_to_role, create_default_roles,
                    remove_all_role_mappings)


class TestStatisticsAPI(APITestCase, TestUtilsMixin):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        cls.other_user_name = 'other_user_name'
        cls.other_user_pass = 'other_user_pass'
        create_default_roles()
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')

        other_user = User.objects.create_user(username=cls.other_user_name,
                                              password=cls.other_user_pass,
                                              email='bar@buzz.com')

        cls.project = mommy.make(
            _model='TextClassificationProject',
            project_type=DOCUMENT_CLASSIFICATION,
            users=[super_user]
        )
        doc1 = mommy.make('Example', project=cls.project)
        doc2 = mommy.make('Example', project=cls.project)
        mommy.make('Category', example=doc1, user=super_user)
        mommy.make('Category', example=doc2, user=other_user)
        cls.url = reverse(viewname='statistics', args=[cls.project.id])
        cls.doc = Example.objects.filter(project=cls.project)

        assign_user_to_role(project_member=other_user, project=cls.project,
                            role_name=settings.ROLE_ANNOTATOR)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()

    def test_returns_exact_progress(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['remaining'], 1)

    def test_returns_exact_progress_with_collaborative_annotation(self):
        self._patch_project(self.project, 'collaborative_annotation', True)

        self.client.login(username=self.other_user_name,
                          password=self.other_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['total'], 2)
        self.assertEqual(response.data['remaining'], 0)

    def test_returns_user_count(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertIn('label', response.data)
        self.assertIsInstance(response.data['label'], dict)

    def test_returns_label_count(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertIn('user', response.data)
        self.assertIsInstance(response.data['user'], dict)

    def test_returns_partial_response(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(f'{self.url}?include=user', format='json')
        self.assertEqual(list(response.data.keys()), ['user'])
