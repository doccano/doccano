import os

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy

from ..models import User, SequenceAnnotation, Document, Role, RoleMapping
from ..models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ, SPEECH2TEXT
from ..utils import PlainTextParser, CoNLLParser, JSONParser, CSVParser, FastTextParser
from ..exceptions import FileParseException
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def create_default_roles():
    Role.objects.get_or_create(name=settings.ROLE_PROJECT_ADMIN)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATOR)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATION_APPROVER)


def assign_user_to_role(project_member, project, role_name):
    role, _ = Role.objects.get_or_create(name=role_name)
    RoleMapping.objects.get_or_create(role_id=role.id, user_id=project_member.id, project_id=project.id)


def remove_all_role_mappings():
    RoleMapping.objects.all().delete()


class TestHealthEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(viewname='health')

    def test_returns_green_status_on_health_endpoint(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['status'], 'green')


class TestUtilsMixin:
    def _patch_project(self, project, attribute, value):
        old_value = getattr(project, attribute, None)
        setattr(project, attribute, value)
        project.save()

        def cleanup_project():
            setattr(project, attribute, old_value)
            project.save()

        self.addCleanup(cleanup_project)


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

    def test_disallows_project_member_to_create_project(self):
        self.client.login(username=self.main_project_member_name,
                          password=self.main_project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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


class TestDocumentListAPI(APITestCase, TestUtilsMixin):

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
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')

        cls.main_project = mommy.make('TextClassificationProject', users=[project_member, super_user])
        doc1 = mommy.make('Document', project=cls.main_project)
        doc2 = mommy.make('Document', project=cls.main_project)
        mommy.make('Document', project=cls.main_project)

        cls.random_order_project = mommy.make('TextClassificationProject', users=[project_member, super_user],
                                              randomize_document_order=True)
        mommy.make('Document', 100, project=cls.random_order_project)

        sub_project = mommy.make('TextClassificationProject', users=[non_project_member])
        mommy.make('Document', project=sub_project)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.random_order_project_url = reverse(viewname='doc_list', args=[cls.random_order_project.id])
        cls.data = {'text': 'example'}
        assign_user_to_role(project_member=project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=project_member, project=cls.random_order_project,
                            role_name=settings.ROLE_ANNOTATOR)

        mommy.make('DocumentAnnotation', document=doc1, user=project_member)
        mommy.make('DocumentAnnotation', document=doc2, user=project_member)

    def _test_list(self, url, username, password, expected_num_results):
        self.client.login(username=username, password=password)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), expected_num_results)

    def test_returns_docs_to_project_member(self):
        self._test_list(self.url,
                        username=self.project_member_name,
                        password=self.project_member_pass,
                        expected_num_results=3)

    def test_returns_docs_to_project_member_filtered_to_active(self):
        self._test_list('{}?doc_annotations__isnull=true'.format(self.url),
                        username=self.project_member_name,
                        password=self.project_member_pass,
                        expected_num_results=1)

    def test_returns_docs_to_project_member_filtered_to_completed(self):
        self._test_list('{}?doc_annotations__isnull=false'.format(self.url),
                        username=self.project_member_name,
                        password=self.project_member_pass,
                        expected_num_results=2)

    def test_returns_docs_to_project_member_filtered_to_active_with_collaborative_annotation(self):
        self._test_list('{}?doc_annotations__isnull=true'.format(self.url),
                        username=self.super_user_name,
                        password=self.super_user_pass,
                        expected_num_results=3)

        self._patch_project(self.main_project, 'collaborative_annotation', True)

        self._test_list('{}?doc_annotations__isnull=true'.format(self.url),
                        username=self.super_user_name,
                        password=self.super_user_pass,
                        expected_num_results=1)

    def test_returns_docs_to_project_member_filtered_to_completed_with_collaborative_annotation(self):
        self._test_list('{}?doc_annotations__isnull=false'.format(self.url),
                        username=self.super_user_name,
                        password=self.super_user_pass,
                        expected_num_results=0)

        self._patch_project(self.main_project, 'collaborative_annotation', True)

        self._test_list('{}?doc_annotations__isnull=false'.format(self.url),
                        username=self.super_user_name,
                        password=self.super_user_pass,
                        expected_num_results=2)

    def test_returns_docs_in_consistent_order_for_all_users(self):
        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        user1_documents = self.client.get(self.url, format='json').json().get('results')
        self.client.logout()

        self.client.login(username=self.super_user_name, password=self.super_user_pass)
        user2_documents = self.client.get(self.url, format='json').json().get('results')
        self.client.logout()

        self.assertEqual([doc['id'] for doc in user1_documents], [doc['id'] for doc in user2_documents])

    def test_can_return_docs_in_consistent_random_order(self):
        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        user1_documents1 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        user1_documents2 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        self.client.logout()
        self.assertEqual(user1_documents1, user1_documents2)

        self.client.login(username=self.super_user_name, password=self.super_user_pass)
        user2_documents1 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        user2_documents2 = self.client.get(self.random_order_project_url, format='json').json().get('results')
        self.client.logout()
        self.assertEqual(user2_documents1, user2_documents2)

        self.assertNotEqual(user1_documents1, user2_documents1)
        self.assertNotEqual(user1_documents2, user2_documents2)

    def test_do_not_return_docs_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_docs_of_other_projects(self):
        self._test_list(self.url,
                        username=self.project_member_name,
                        password=self.project_member_pass,
                        expected_num_results=self.main_project.documents.count())

    def test_allows_superuser_to_create_doc(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_project_member_to_create_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestDocumentDetailAPI(APITestCase):

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
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        project = mommy.make('TextClassificationProject', users=[project_member, super_user])
        cls.doc = mommy.make('Document', project=project)
        cls.url = reverse(viewname='doc_detail', args=[project.id, cls.doc.id])
        cls.data = {'text': 'example'}
        assign_user_to_role(project_member=project_member, project=project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_returns_doc_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.doc.id)

    def test_do_not_return_doc_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_update_doc(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_disallows_project_member_to_update_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_delete_doc(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_doc(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestApproveLabelsAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.annotator_name = 'annotator_name'
        cls.annotator_pass = 'annotator_pass'
        cls.approver_name = 'approver_name_name'
        cls.approver_pass = 'approver_pass'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        annotator = User.objects.create_user(username=cls.annotator_name,
                                             password=cls.annotator_pass)
        approver = User.objects.create_user(username=cls.approver_name,
                                            password=cls.approver_pass)
        project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                 password=cls.project_admin_pass)
        project = mommy.make('TextClassificationProject', users=[annotator, approver, project_admin])
        cls.doc = mommy.make('Document', project=project)
        cls.url = reverse(viewname='approve_labels', args=[project.id, cls.doc.id])
        create_default_roles()
        assign_user_to_role(project_member=annotator, project=project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=approver, project=project,
                            role_name=settings.ROLE_ANNOTATION_APPROVER)
        assign_user_to_role(project_member=project_admin, project=project,
                            role_name=settings.ROLE_PROJECT_ADMIN)

    def test_allow_project_admin_to_approve_and_disapprove_labels(self):
        self.client.login(username=self.project_admin_name, password=self.project_admin_pass)

        response = self.client.post(self.url, format='json', data={'approved': True})
        self.assertEqual(response.data['annotation_approver'], self.project_admin_name)

        response = self.client.post(self.url, format='json', data={'approved': False})
        self.assertIsNone(response.data['annotation_approver'])

    def test_allow_approver_to_approve_and_disapprove_labels(self):
        self.client.login(username=self.approver_name, password=self.approver_pass)

        response = self.client.post(self.url, format='json', data={'approved': True})
        self.assertEqual(response.data['annotation_approver'], self.approver_name)

        response = self.client.post(self.url, format='json', data={'approved': False})
        self.assertIsNone(response.data['annotation_approver'])

    def test_disallows_non_annotation_approver_to_approve_and_disapprove_labels(self):
        self.client.login(username=self.annotator_name, password=self.annotator_pass)

        response = self.client.post(self.url, format='json', data={'approved': True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestAnnotationListAPI(APITestCase, TestUtilsMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        main_project = mommy.make('SequenceLabelingProject', users=[project_member, another_project_member])
        main_project_label = mommy.make('Label', project=main_project)
        main_project_doc = mommy.make('Document', project=main_project)
        mommy.make('SequenceAnnotation', document=main_project_doc, user=project_member)
        mommy.make('SequenceAnnotation', document=main_project_doc, user=another_project_member)

        sub_project = mommy.make('SequenceLabelingProject', users=[non_project_member])
        sub_project_doc = mommy.make('Document', project=sub_project)
        mommy.make('SequenceAnnotation', document=sub_project_doc)

        cls.classification_project = mommy.make('TextClassificationProject',
                                                users=[project_member, another_project_member])
        cls.classification_project_label_1 = mommy.make('Label', project=cls.classification_project)
        cls.classification_project_label_2 = mommy.make('Label', project=cls.classification_project)
        cls.classification_project_document = mommy.make('Document', project=cls.classification_project)
        cls.classification_project_url = reverse(
            viewname='annotation_list', args=[cls.classification_project.id, cls.classification_project_document.id])
        assign_user_to_role(project_member=project_member, project=cls.classification_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=another_project_member, project=cls.classification_project,
                            role_name=settings.ROLE_ANNOTATOR)

        cls.url = reverse(viewname='annotation_list', args=[main_project.id, main_project_doc.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 1, 'label': main_project_label.id}
        cls.num_entity_of_project_member = SequenceAnnotation.objects.filter(document=main_project_doc,
                                                                             user=project_member).count()
        cls.num_entity_of_another_project_member = SequenceAnnotation.objects.filter(
            document=main_project_doc,
            user=another_project_member).count()
        cls.main_project = main_project
        assign_user_to_role(project_member=project_member, project=main_project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_returns_annotations_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_annotations_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_annotations_of_another_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data), self.num_entity_of_project_member)

    def test_returns_annotations_of_another_project_member_if_collaborative_project(self):
        self._patch_project(self.main_project, 'collaborative_annotation', True)

        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.data),
                         self.num_entity_of_project_member + self.num_entity_of_another_project_member)

    def test_allows_project_member_to_create_annotation(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_disallows_non_project_member_to_create_annotation(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.post(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_second_annotation_for_single_class_project(self):
        self._patch_project(self.classification_project, 'single_class_classification', True)

        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_disallows_second_annotation_for_single_class_shared_project(self):
        self._patch_project(self.classification_project, 'single_class_classification', True)
        self._patch_project(self.classification_project, 'collaborative_annotation', True)

        self.client.login(username=self.project_member_name, password=self.project_member_pass)
        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_1.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(username=self.another_project_member_name, password=self.another_project_member_pass)
        response = self.client.post(self.classification_project_url, format='json',
                                    data={'label': self.classification_project_label_2.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _patch_project(self, project, attribute, value):
        old_value = getattr(project, attribute, None)
        setattr(project, attribute, value)
        project.save()

        def cleanup_project():
            setattr(project, attribute, old_value)
            project.save()

        self.addCleanup(cleanup_project)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestAnnotationDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        # Todo: change super_user to project_admin.
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        main_project = mommy.make('SequenceLabelingProject',
                                  users=[super_user, project_member, another_project_member])
        main_project_doc = mommy.make('Document', project=main_project)
        main_project_entity = mommy.make('SequenceAnnotation',
                                         document=main_project_doc, user=project_member)
        another_entity = mommy.make('SequenceAnnotation',
                                    document=main_project_doc, user=another_project_member)

        shared_project = mommy.make('SequenceLabelingProject',
                                    collaborative_annotation=True,
                                    users=[project_member, another_project_member])
        shared_project_doc = mommy.make('Document', project=shared_project)
        shared_entity = mommy.make('SequenceAnnotation', document=shared_project_doc, user=another_project_member)

        cls.url = reverse(viewname='annotation_detail', args=[main_project.id,
                                                              main_project_doc.id,
                                                              main_project_entity.id])
        cls.another_url = reverse(viewname='annotation_detail', args=[main_project.id,
                                                                      main_project_doc.id,
                                                                      another_entity.id])
        cls.shared_url = reverse(viewname='annotation_detail', args=[shared_project.id,
                                                                     shared_project_doc.id,
                                                                     shared_entity.id])
        cls.post_data = {'start_offset': 0, 'end_offset': 10}
        assign_user_to_role(project_member=project_member, project=main_project, role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=project_member, project=shared_project, role_name=settings.ROLE_ANNOTATOR)

    def test_returns_annotation_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_annotation_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_annotation_by_another_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.another_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_update_annotation(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_disallows_non_project_member_to_update_annotation(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_project_member_to_update_annotation_of_another_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.another_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_superuser_to_delete_annotation_of_another_member(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.delete(self.another_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_allows_project_member_to_delete_annotation(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_annotation(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallows_project_member_to_delete_annotation_of_another_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.another_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allow_member_to_update_others_annotation_in_shared_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.shared_url, format='json', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allow_member_to_delete_others_annotation_in_shared_project(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.shared_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestCommentListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.another_project_member_name = 'another_project_member_name'
        cls.another_project_member_pass = 'another_project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        cls.project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        another_project_member = User.objects.create_user(username=cls.another_project_member_name,
                                                          password=cls.another_project_member_pass)
        User.objects.create_user(username=cls.non_project_member_name, password=cls.non_project_member_pass)

        main_project = mommy.make('SequenceLabelingProject', users=[cls.project_member, another_project_member])
        main_project_doc = mommy.make('Document', project=main_project)
        cls.comment = mommy.make('Comment', document=main_project_doc, text='comment 1', user=cls.project_member)
        mommy.make('Comment', document=main_project_doc, text='comment 2', user=cls.project_member)
        mommy.make('Comment', document=main_project_doc, text='comment 3', user=another_project_member)

        cls.url = reverse(viewname='comment_list', args=[main_project.id, main_project_doc.id])

        assign_user_to_role(project_member=cls.project_member, project=main_project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=another_project_member, project=main_project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_returns_own_comments_to_project_member(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        self.client.login(username=self.another_project_member_name,
                          password=self.another_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_does_not_return_comments_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_allow_deletion_by_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.delete('{}/{}'.format(self.url, self.comment.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_does_not_allow_deletion_of_non_owned_comment(self):
        self.client.login(username=self.another_project_member_name,
                          password=self.another_project_member_pass)
        response = self.client.delete('{}/{}'.format(self.url, self.comment.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_update_delete_comment(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data={'text': 'comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.project_member.id)
        self.assertEqual(response.data['text'], 'comment')
        url = '{}/{}'.format(self.url, response.data['id'])

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

        response = self.client.patch(url, format='json', data={'text': 'new comment'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'new comment')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestSearch(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        non_project_member = User.objects.create_user(username=cls.non_project_member_name,
                                                      password=cls.non_project_member_pass)

        cls.main_project = mommy.make('TextClassificationProject', users=[project_member])
        cls.search_term = 'example'
        doc1 = mommy.make('Document', text=cls.search_term, project=cls.main_project)
        doc2 = mommy.make('Document', text='Lorem', project=cls.main_project)
        label1 = mommy.make('Label', project=cls.main_project)
        label2 = mommy.make('Label', project=cls.main_project)
        mommy.make('SequenceAnnotation', document=doc1, user=project_member, label=label1)
        mommy.make('SequenceAnnotation', document=doc2, user=project_member, label=label2)

        sub_project = mommy.make('TextClassificationProject', users=[non_project_member])
        mommy.make('Document', text=cls.search_term, project=sub_project)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.data = {'q': cls.search_term}
        assign_user_to_role(project_member=project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_can_filter_doc_by_term(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=self.data)
        count = Document.objects.filter(text__contains=self.search_term,
                                        project=self.main_project).count()
        self.assertEqual(response.data['count'], count)

    def test_can_order_doc_by_created_at_ascending(self):
        params = {'ordering': 'created_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('created_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_order_doc_by_created_at_descending(self):
        params = {'ordering': '-created_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('-created_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_order_doc_by_annotation_updated_at_ascending(self):
        params = {'ordering': 'seq_annotations__updated_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('seq_annotations__updated_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_order_doc_by_annotation_updated_at_descending(self):
        params = {'ordering': '-seq_annotations__updated_at'}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project).order_by('-seq_annotations__updated_at').values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestFilter(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                  password=cls.project_member_pass)
        cls.main_project = mommy.make('SequenceLabelingProject', users=[project_member])
        cls.label1 = mommy.make('Label', project=cls.main_project)
        cls.label2 = mommy.make('Label', project=cls.main_project)
        doc1 = mommy.make('Document', project=cls.main_project)
        doc2 = mommy.make('Document', project=cls.main_project)
        mommy.make('Document', project=cls.main_project)
        mommy.make('SequenceAnnotation', document=doc1, user=project_member, label=cls.label1)
        mommy.make('SequenceAnnotation', document=doc2, user=project_member, label=cls.label2)
        cls.url = reverse(viewname='doc_list', args=[cls.main_project.id])
        cls.params = {'seq_annotations__label__id': cls.label1.id}
        assign_user_to_role(project_member=project_member, project=cls.main_project,
                            role_name=settings.ROLE_ANNOTATOR)

    def test_can_filter_by_label(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=self.params)
        docs = Document.objects.filter(project=self.main_project,
                                       seq_annotations__label__id=self.label1.id).values()
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_filter_doc_with_annotation(self):
        params = {'seq_annotations__isnull': False}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project, seq_annotations__isnull=False).values()
        self.assertEqual(response.data['count'], docs.count())
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    def test_can_filter_doc_without_anotation(self):
        params = {'seq_annotations__isnull': True}
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json', data=params)
        docs = Document.objects.filter(project=self.main_project, seq_annotations__isnull=True).values()
        self.assertEqual(response.data['count'], docs.count())
        for d1, d2 in zip(response.data['results'], docs):
            self.assertEqual(d1['id'], d2['id'])

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


class TestUploader(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        # Todo: change super_user to project_admin.
        create_default_roles()
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.classification_project = mommy.make('TextClassificationProject',
                                                users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
        cls.labeling_project = mommy.make('SequenceLabelingProject',
                                          users=[super_user], project_type=SEQUENCE_LABELING)
        cls.seq2seq_project = mommy.make('Seq2seqProject', users=[super_user], project_type=SEQ2SEQ)
        assign_user_to_role(project_member=super_user, project=cls.classification_project,
                            role_name=settings.ROLE_PROJECT_ADMIN)
        assign_user_to_role(project_member=super_user, project=cls.labeling_project,
                            role_name=settings.ROLE_PROJECT_ADMIN)
        assign_user_to_role(project_member=super_user, project=cls.seq2seq_project,
                            role_name=settings.ROLE_PROJECT_ADMIN)

    def setUp(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)

    def upload_test_helper(self, project_id, filename, file_format, expected_status, **kwargs):
        url = reverse(viewname='doc_uploader', args=[project_id])

        with open(os.path.join(DATA_DIR, filename), 'rb') as f:
            response = self.client.post(url, data={'file': f, 'format': file_format})

        self.assertEqual(response.status_code, expected_status)

    def label_test_helper(self, project_id, expected_labels, expected_label_keys):
        url = reverse(viewname='label_list', args=[project_id])
        expected_keys = {key for label in expected_labels for key in label}

        response = self.client.get(url).json()

        actual_labels = [{key: value for (key, value) in label.items() if key in expected_keys}
                         for label in response]

        self.assertCountEqual(actual_labels, expected_labels)

        for label in response:
            for expected_label_key in expected_label_keys:
                self.assertIsNotNone(label.get(expected_label_key))

    def test_can_upload_conll_format_file(self):
        self.upload_test_helper(project_id=self.labeling_project.id,
                                filename='labeling.conll',
                                file_format='conll',
                                expected_status=status.HTTP_201_CREATED)

    def test_cannot_upload_wrong_conll_format_file(self):
        self.upload_test_helper(project_id=self.labeling_project.id,
                                filename='labeling.invalid.conll',
                                file_format='conll',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_upload_classification_csv(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_classification_csv_with_out_of_order_columns(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example_out_of_order_columns.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

        self.label_test_helper(
            project_id=self.classification_project.id,
            expected_labels=[
                {'text': 'Positive'},
                {'text': 'Negative'},
            ],
            expected_label_keys=[],
        )

    def test_can_upload_csv_with_non_utf8_encoding(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.utf16.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_seq2seq_csv(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='example.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_single_column_csv(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='example_one_column.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_csv_file_does_not_match_column_and_row(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example_column_and_row_not_matching.csv',
                                file_format='csv',
                                expected_status=status.HTTP_201_CREATED)

    def test_cannot_upload_csv_file_has_too_many_columns(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.invalid.2.csv',
                                file_format='csv',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_upload_classification_excel(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.xlsx',
                                file_format='excel',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_seq2seq_excel(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='example.xlsx',
                                file_format='excel',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_single_column_excel(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='example_one_column.xlsx',
                                file_format='excel',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_excel_file_does_not_match_column_and_row(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example_column_and_row_not_matching.xlsx',
                                file_format='excel',
                                expected_status=status.HTTP_201_CREATED)

    def test_cannot_upload_excel_file_has_too_many_columns(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.invalid.2.xlsx',
                                file_format='excel',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    @override_settings(IMPORT_BATCH_SIZE=1)
    def test_can_upload_small_batch_size(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='example_one_column_no_header.xlsx',
                                file_format='excel',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_classification_jsonl(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='classification.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

        self.label_test_helper(
            project_id=self.classification_project.id,
            expected_labels=[
                {'text': 'positive', 'suffix_key': 'p', 'prefix_key': None},
                {'text': 'negative', 'suffix_key': 'n', 'prefix_key': None},
                {'text': 'neutral', 'suffix_key': 'n', 'prefix_key': 'ctrl'},
            ],
            expected_label_keys=[
                'background_color',
                'text_color',
            ])

    def test_can_upload_labeling_jsonl(self):
        self.upload_test_helper(project_id=self.labeling_project.id,
                                filename='labeling.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

        self.label_test_helper(
            project_id=self.labeling_project.id,
            expected_labels=[
                {'text': 'LOC', 'suffix_key': 'l', 'prefix_key': None},
                {'text': 'ORG', 'suffix_key': 'o', 'prefix_key': None},
                {'text': 'PER', 'suffix_key': 'p', 'prefix_key': None},
            ],
            expected_label_keys=[
                'background_color',
                'text_color',
            ])

    def test_can_upload_seq2seq_jsonl(self):
        self.upload_test_helper(project_id=self.seq2seq_project.id,
                                filename='seq2seq.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_plain_text(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.txt',
                                file_format='plain',
                                expected_status=status.HTTP_201_CREATED)

    def test_can_upload_data_without_label(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)

    @classmethod
    def doCleanups(cls):
        remove_all_role_mappings()


@override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER='LOCAL')
@override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_ACCOUNT=os.path.dirname(DATA_DIR))
@override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_SECRET_KEY='not-used')
class TestCloudUploader(TestUploader):
    def upload_test_helper(self, project_id, filename, file_format, expected_status, **kwargs):
        query_params = {
            'project_id': project_id,
            'upload_format': file_format,
            'container': kwargs.pop('container', os.path.basename(DATA_DIR)),
            'object': filename,
        }

        query_params.update(kwargs)

        response = self.client.get(reverse('cloud_uploader'), query_params)

        self.assertEqual(response.status_code, expected_status)

    def test_cannot_upload_with_missing_file(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='does-not-exist',
                                file_format='json',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_cannot_upload_with_missing_container(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                container='does-not-exist',
                                file_format='json',
                                expected_status=status.HTTP_400_BAD_REQUEST)

    def test_cannot_upload_with_missing_query_parameters(self):
        response = self.client.get(reverse('cloud_uploader'), {'project_id': self.classification_project.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_upload_with_redirect(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                next='http://somewhere',
                                file_format='json',
                                expected_status=status.HTTP_302_FOUND)

    def test_can_upload_with_redirect_to_blank(self):
        self.upload_test_helper(project_id=self.classification_project.id,
                                filename='example.jsonl',
                                next='about:blank',
                                file_format='json',
                                expected_status=status.HTTP_201_CREATED)


class TestFeatures(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_name = 'user_name'
        cls.user_pass = 'user_pass'
        create_default_roles()
        cls.user = User.objects.create_user(username=cls.user_name, password=cls.user_pass, email='fizz@buzz.com')

    def setUp(self):
        self.client.login(username=self.user_name, password=self.user_pass)

    @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER=None)
    def test_no_cloud_upload(self):
        response = self.client.get(reverse('features'))

        self.assertFalse(response.json().get('cloud_upload'))


@override_settings(IMPORT_BATCH_SIZE=2)
class TestParser(APITestCase):

    def parser_helper(self, filename, parser, include_label=True):
        with open(os.path.join(DATA_DIR, filename), mode='rb') as f:
            result = list(parser.parse(f))
            for data in result:
                for r in data:
                    self.assertIn('text', r)
                    if include_label:
                        self.assertIn('labels', r)
        return result

    def test_give_valid_data_to_conll_parser(self):
        self.parser_helper(filename='labeling.conll', parser=CoNLLParser())

    def test_give_valid_data_to_conll_parser_with_trailing_newlines(self):
        result = self.parser_helper(filename='labeling.trailing.conll', parser=CoNLLParser())
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)

    def test_plain_parser(self):
        self.parser_helper(filename='example.txt', parser=PlainTextParser(), include_label=False)

    def test_give_invalid_data_to_conll_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='labeling.invalid.conll',
                               parser=CoNLLParser())

    def test_give_classification_data_to_csv_parser(self):
        self.parser_helper(filename='example.csv', parser=CSVParser(), include_label=False)

    def test_give_seq2seq_data_to_csv_parser(self):
        self.parser_helper(filename='example.csv', parser=CSVParser(), include_label=False)

    def test_give_classification_data_to_json_parser(self):
        self.parser_helper(filename='classification.jsonl', parser=JSONParser())

    def test_give_labeling_data_to_json_parser(self):
        self.parser_helper(filename='labeling.jsonl', parser=JSONParser())

    def test_give_seq2seq_data_to_json_parser(self):
        self.parser_helper(filename='seq2seq.jsonl', parser=JSONParser())

    def test_give_data_without_label_to_json_parser(self):
        self.parser_helper(filename='example.jsonl', parser=JSONParser(), include_label=False)

    def test_give_labeling_data_to_fasttext_parser(self):
        self.parser_helper(filename='example_fasttext.txt', parser=FastTextParser())

    def test_give_data_without_label_name_to_fasttext_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='example_fasttext_label_tag_without_name.txt', parser=FastTextParser())

    def test_give_data_without_text_to_fasttext_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='example_fasttext_without_text.txt', parser=FastTextParser())


class TestDownloader(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        # Todo: change super_user to project_admin.
        create_default_roles()
        super_user = User.objects.create_superuser(username=cls.super_user_name,
                                                   password=cls.super_user_pass,
                                                   email='fizz@buzz.com')
        cls.classification_project = mommy.make('TextClassificationProject',
                                                users=[super_user], project_type=DOCUMENT_CLASSIFICATION)
        cls.labeling_project = mommy.make('SequenceLabelingProject',
                                          users=[super_user], project_type=SEQUENCE_LABELING)
        cls.seq2seq_project = mommy.make('Seq2seqProject', users=[super_user], project_type=SEQ2SEQ)
        cls.speech2text_project = mommy.make('Speech2textProject', users=[super_user], project_type=SPEECH2TEXT)
        cls.classification_url = reverse(viewname='doc_downloader', args=[cls.classification_project.id])
        cls.labeling_url = reverse(viewname='doc_downloader', args=[cls.labeling_project.id])
        cls.seq2seq_url = reverse(viewname='doc_downloader', args=[cls.seq2seq_project.id])
        cls.speech2text_url = reverse(viewname='doc_downloader', args=[cls.speech2text_project.id])

    def setUp(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)

    def download_test_helper(self, url, format, expected_status):
        response = self.client.get(url, data={'q': format})
        self.assertEqual(response.status_code, expected_status)

    def test_cannot_download_conll_format_file(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='conll',
                                  expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_download_classification_csv(self):
        self.download_test_helper(url=self.classification_url,
                                  format='csv',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_labeling_csv(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='csv',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_seq2seq_csv(self):
        self.download_test_helper(url=self.seq2seq_url,
                                  format='csv',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_classification_jsonl(self):
        self.download_test_helper(url=self.classification_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_labeling_jsonl(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_seq2seq_jsonl(self):
        self.download_test_helper(url=self.seq2seq_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_speech2text_jsonl(self):
        self.download_test_helper(url=self.speech2text_url,
                                  format='json',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_labelling_jsonl(self):
        self.download_test_helper(url=self.labeling_url,
                                  format='jsonl',
                                  expected_status=status.HTTP_200_OK)

    def test_can_download_plain_text(self):
        self.download_test_helper(url=self.classification_url,
                                  format='plain',
                                  expected_status=status.HTTP_400_BAD_REQUEST)

    def test_can_download_classification_fasttext(self):
        self.download_test_helper(url=self.classification_url,
                                    format='txt',
                                    expected_status=status.HTTP_200_OK)


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

        cls.project = mommy.make('TextClassificationProject', users=[super_user, other_user])
        doc1 = mommy.make('Document', project=cls.project)
        doc2 = mommy.make('Document', project=cls.project)
        mommy.make('DocumentAnnotation', document=doc1, user=super_user)
        mommy.make('DocumentAnnotation', document=doc2, user=other_user)
        cls.url = reverse(viewname='statistics', args=[cls.project.id])
        cls.doc = Document.objects.filter(project=cls.project)

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


class TestUserAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user_name = 'super_user_name'
        cls.super_user_pass = 'super_user_pass'
        create_default_roles()
        User.objects.create_superuser(username=cls.super_user_name,
                                      password=cls.super_user_pass,
                                      email='fizz@buzz.com')
        cls.url = reverse(viewname='user_list')

    def test_returns_user_count(self):
        self.client.login(username=self.super_user_name,
                          password=self.super_user_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(1, len(response.data))


class TestRoleAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_name = 'user_name'
        cls.user_pass = 'user_pass'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        create_default_roles()
        cls.user = User.objects.create_user(username=cls.user_name,
                                            password=cls.user_pass)
        User.objects.create_superuser(username=cls.project_admin_name,
                                      password=cls.project_admin_pass,
                                      email='fizz@buzz.com')
        cls.url = reverse(viewname='roles')

    def test_cannot_create_multiple_roles_with_same_name(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        roles = [
            {'name': 'examplerole', 'description': 'example'},
            {'name': 'examplerole', 'description': 'example'}
        ]
        self.client.post(self.url, format='json', data=roles[0])
        second_response = self.client.post(self.url, format='json', data=roles[1])
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonadmin_cannot_create_role(self):
        self.client.login(username=self.user_name,
                          password=self.user_pass)
        data = {'name': 'testrole', 'description': 'example'}
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_role(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        data = {'name': 'testrole', 'description': 'example'}
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_get_roles(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRoleMappingListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.second_project_member_name = 'second_project_member_name'
        cls.second_project_member_pass = 'second_project_member_pass'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        create_default_roles()
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        cls.second_project_member = User.objects.create_user(username=cls.second_project_member_name,
                                                      password=cls.second_project_member_pass)
        project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                   password=cls.project_admin_pass)
        cls.main_project = mommy.make('Project', users=[project_member, project_admin, cls.second_project_member])
        cls.other_project = mommy.make('Project', users=[cls.second_project_member, project_admin])
        cls.admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        cls.role = mommy.make('Role', name='otherrole')
        mommy.make('RoleMapping', role=cls.admin_role, project=cls.main_project, user=project_admin)
        cls.data = {'user': project_member.id, 'role': cls.admin_role.id, 'project': cls.main_project.id}
        cls.other_url = reverse(viewname='rolemapping_list', args=[cls.other_project.id])
        cls.url = reverse(viewname='rolemapping_list', args=[cls.main_project.id])

    def test_returns_mappings_to_project_admin(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_allows_superuser_to_create_mapping(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_do_not_allow_nonadmin_to_create_mapping(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.post(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_do_not_return_mappings_to_nonadmin(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRoleMappingDetailAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        cls.project_member_name = 'project_member_name'
        cls.project_member_pass = 'project_member_pass'
        cls.non_project_member_name = 'non_project_member_name'
        cls.non_project_member_pass = 'non_project_member_pass'
        create_default_roles()
        project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                   password=cls.project_admin_pass)
        project_member = User.objects.create_user(username=cls.project_member_name,
                                                      password=cls.project_member_pass)
        User.objects.create_user(username=cls.non_project_member_name, password=cls.non_project_member_pass)
        project = mommy.make('Project', users=[project_admin, project_member])
        admin_role = Role.objects.get(name=settings.ROLE_PROJECT_ADMIN)
        annotator_role = Role.objects.get(name=settings.ROLE_ANNOTATOR)
        cls.rolemapping = mommy.make('RoleMapping', role=admin_role, project=project, user=project_admin)
        cls.url = reverse(viewname='rolemapping_detail', args=[project.id, cls.rolemapping.id])
        cls.data = {'role': annotator_role.id }

    def test_returns_rolemapping_to_project_member(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['id'], self.rolemapping.id)

    def test_do_not_return_mapping_to_non_project_member(self):
        self.client.login(username=self.non_project_member_name,
                          password=self.non_project_member_pass)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_update_mapping(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.data['role'], self.data['role'])

    def test_disallows_project_member_to_update_mapping(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.patch(self.url, format='json', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_delete_mapping(self):
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_disallows_project_member_to_delete_mapping(self):
        self.client.login(username=self.project_member_name,
                          password=self.project_member_pass)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
