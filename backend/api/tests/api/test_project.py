from django.conf import settings
from django.contrib.auth.models import User
from django.test import override_settings
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import (assign_user_to_role, create_default_roles,
                    remove_all_role_mappings)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestProjectListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.main_project_member_name = 'project_member_name'
        cls.main_project_member_pass = 'project_member_pass'
        cls.sub_project_member_name = 'sub_project_member_name'
        cls.sub_project_member_pass = 'sub_project_member_pass'
        cls.approver_name = 'approver_name_name'
        cls.approver_pass = 'approver_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        create_default_roles()
        main_project_member = User.objects.create_user(username=cls.main_project_member_name,
                                                       password=cls.main_project_member_pass)
        sub_project_member = User.objects.create_user(username=cls.sub_project_member_name,
                                                      password=cls.sub_project_member_pass)
        approver = User.objects.create_user(username=cls.approver_name,
                                            password=cls.approver_pass)
        User.objects.create_superuser(username=cls.super_user_name,
                                      password=cls.super_user_pass,
                                      email='fizz@buzz.com')
        cls.main_project = mommy.make('TextClassificationProject', users=[main_project_member])
        cls.sub_project = mommy.make('TextClassificationProject', users=[sub_project_member])
        assign_user_to_role(project_member=main_project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=sub_project_member, project=cls.sub_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=approver, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATION_APPROVER)
        cls.url = reverse(viewname='project_list')
        cls.data = {'name': 'example', 'project_type': 'DocumentClassification',
                    'description': 'example', 'guideline': 'example',
                    'resourcetype': 'TextClassificationProject'}
        cls.num_project = main_project_member.projects.count()

    def test_returns_main_project_to_approver(self):
        self.client.login(username=self.approver_name,
                          password=self.approver_pass)
        response = self.client.get(self.url, format='json')
        project = response.data[0]
        num_project = len(response.data)
        self.assertEqual(num_project, self.num_project)
        self.assertEqual(project['id'], self.main_project.id)

    def test_returns_main_project_to_main_project_member(self):
        self.client.login(username=self.main_project_member_name,
                          password=self.main_project_member_pass)
        response = self.client.get(self.url, format='json')
        project = response.data[0]
        num_project = len(response.data)
        self.assertEqual(num_project, self.num_project)
        self.assertEqual(project['id'], self.main_project.id)

    def test_do_not_return_main_project_to_sub_project_member(self):
        self.client.login(username=self.sub_project_member_name,
                          password=self.sub_project_member_pass)
        response = self.client.get(self.url, format='json')
        project = response.data[0]
        num_project = len(response.data)
        self.assertEqual(num_project, self.num_project)
        self.assertNotEqual(project['id'], self.main_project.id)

    def test_allows_superuser_to_create_project(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.json().get('collaborative_annotation'))
        self.assertFalse(response.json().get('randomize_document_order'))

    def test_allows_superuser_to_create_project_with_flags(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        data = dict(self.data)
        data['collaborative_annotation'] = True
        data['randomize_document_order'] = True
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json().get('collaborative_annotation'))
        self.assertTrue(response.json().get('randomize_document_order'))

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestProjectDetailAPI(APITestCase):

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

        cls.main_project = mommy.make('TextClassificationProject', users=[cls.project_member, project_admin])
        mommy.make('TextClassificationProject', users=[non_project_member])
        cls.url = reverse(viewname='project_detail', args=[cls.main_project.id])
        cls.data = {'description': 'lorem'}
        assign_user_to_role(project_member=cls.project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=project_admin, project=cls.main_project,
                            role_name=settings.ROLE_PROJECT_ADMIN)

    def test_returns_main_project_detail_to_main_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.main_project.id)

    def test_do_not_return_main_project_to_sub_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_update_project(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['description'], self.data['description'])

    def test_disallows_non_project_member_to_update_project(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_delete_project(self):
        self.client.login(username=self.admin_user_name,
                          password=self.admin_user_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_non_project_member_to_delete_project(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestTagAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.main_project_member_name = 'project_member_name'
        cls.main_project_member_pass = 'project_member_pass'
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        create_default_roles()
        main_project_member = User.objects.create_user(username=cls.main_project_member_name,
                                                       password=cls.main_project_member_pass)
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                      password=cls.super_user_pass,
                                      email='fizz@buzz.com')
        cls.main_project = mommy.make('TextClassificationProject', users=[main_project_member, super_user])
        assign_user_to_role(project_member=main_project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=super_user, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        cls.tag = mommy.make('Tag', project=cls.main_project, text='Tag 1')
        cls.url = reverse(viewname='tag_list', args=[cls.main_project.id])
        cls.project_url = reverse(viewname='project_list')
        cls.delete_url = reverse(viewname='tag_list', args=[cls.main_project.id])

    def test_create_tag(self):
        self.client.login(username=self.super_user_name,
                        password=self.super_user_pass)
        response = self.client.post(self.url, data={'text': 'Tag 2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.project_url, format='json')
        self.assertTrue(response.data[0]['tags'][1]['text'] == 'Tag 2' ,'Content of tags differs.')

    def test_tag_list(self):
        self.client.login(username=self.main_project_member_name,
                        password=self.main_project_member_pass)
        response = self.client.get(self.project_url, format='json')
        self.assertTrue(len(response.data[0]['tags']) == 1 ,'Number of tags differs expected amount.')
        self.assertTrue(response.data[0]['tags'][0]['text'] == 'Tag 1' ,'Content of tags differs.')

    def test_delete_tag(self):
        self.client.login(username=self.super_user_name,
                        password=self.super_user_pass)
        response = self.client.delete(self.delete_url, data={'id': self.tag.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.project_url, format='json')
        self.assertTrue(len(response.data[0]['tags']) == 0 ,'Number of tags differs expected amount.')


    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()
