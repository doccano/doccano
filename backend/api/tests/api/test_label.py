import os

from django.conf import settings
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import (DATA_DIR, assign_user_to_role, create_default_roles,
                    remove_all_role_mappings)


class TestLabelListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.admin_user_name = 'admin_user_name'
        cls.admin_user_pass = 'admin_user_pass'
        create_default_roles()
        cls.project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        project_admin = User.objects.create_superuser(username=cls.admin_user_name,
                                                   password=cls.admin_user_pass,
                                                   email='fizz@buzz.com')
        cls.main_project = mommy.make('Project', users=[cls.project_member, project_admin])
        cls.main_project_label = mommy.make('Label', project=cls.main_project)

        sub_project = mommy.make('Project', users=[non_project_member])
        other_project = mommy.make('Project', users=[project_admin])
        mommy.make('Label', project=sub_project)
        cls.url = reverse(viewname='label_list', args=[cls.main_project.id])
        cls.other_url = reverse(viewname='label_list', args=[other_project.id])
        cls.data = {'text': 'example'}
        assign_user_to_role(project_member=cls.project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_returns_labels_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_labels_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_labels_of_other_projects(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        label = response.data[0]
        num_labels = len(response.data)
        self.assertEqual(num_labels, len(self.main_project.labels.all()))
        self.assertEqual(label['id'], self.main_project_label.id)

    def test_allows_admin_to_create_label(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_multiple_labels_without_shortcut_key(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        labels = [
            {'text': 'Ruby', 'prefix_key': None, 'suffix_key': None},
            {'text': 'PHP', 'prefix_key': None, 'suffix_key': None}
        ]
        for label in labels:
            response = self.client.post(self.url, format='json', data=label)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_same_label_in_multiple_projects(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        label = {'text': 'LOC', 'prefix_key': None, 'suffix_key': 'l'}
        response = self.client.post(self.url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.other_url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_create_same_suffix_with_different_prefix(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        label = {'text': 'Person', 'prefix_key': None, 'suffix_key': 'p'}
        response = self.client.post(self.url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        label = {'text': 'Percentage', 'prefix_key': 'ctrl', 'suffix_key': 'p'}
        response = self.client.post(self.url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_same_shortcut_key(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        label = {'text': 'Person', 'prefix_key': None, 'suffix_key': 'p'}
        response = self.client.post(self.url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        label = {'text': 'Percentage', 'prefix_key': None, 'suffix_key': 'p'}
        response = self.client.post(self.url, format='json', data=label)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_disallows_project_member_to_create_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestLabelDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        User.objects.create_user(username=cls.non_project_member_name, password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        project = mommy.make('Project', users=[project_member, super_user])
        cls.label = mommy.make('Label', project=project)
        cls.label_with_shortcut = mommy.make('Label', suffix_key='l', project=project)
        cls.url = reverse(viewname='label_detail', args=[project.id, cls.label.id])
        cls.url_with_shortcut = reverse(viewname='label_detail', args=[project.id, cls.label_with_shortcut.id])
        cls.data = {'text': 'example'}
        create_default_roles()
        assign_user_to_role(project_member=project_member, project=project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_returns_label_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.label.id)

    def test_do_not_return_label_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_update_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_allows_superuser_to_update_label_with_shortcut(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url_with_shortcut, format='json', data={'suffix_key': 's'})
        self.assertEqual(response.data['suffix_key'], 's')

    def test_disallows_project_member_to_update_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_delete_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestLabelUploadAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        User.objects.create_user(username=cls.non_project_member_name, password=cls.non_project_member_pass)
        project_admin = User.objects.create_user(username=cls.super_user_name,
                                                 password=cls.super_user_pass)
        project = mommy.make('Project', users=[project_member, project_admin])
        cls.url = reverse(viewname='label_upload', args=[project.id])
        create_default_roles()
        assign_user_to_role(project_member=project_admin, project=project, role_name=settings.ROLE_PROJECT_ADMIN)
        assign_user_to_role(project_member=project_member, project=project, role_name=settings.ROLE_ANNOTATOR)

    def help_to_upload_file(self, filename, expected_status):
        with open(os.path.join(DATA_DIR, filename), 'rb') as f:
            response = self.client.post(self.url, data={'file': f})
        self.assertEqual(response.status_code, expected_status)

    def test_allows_project_admin_to_upload_label(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        self.help_to_upload_file('valid_labels.json', status.HTTP_201_CREATED)

    def test_disallows_project_member_to_upload_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        self.help_to_upload_file('valid_labels.json', status.HTTP_403_FORBIDDEN)

    def test_try_to_upload_invalid_file(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        self.help_to_upload_file('invalid_labels.json', status.HTTP_400_BAD_REQUEST)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()
