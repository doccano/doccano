from django.conf import settings
from django.contrib.auth.models import User
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Document
from .utils import (TestUtilsMixin, assign_user_to_role, create_default_roles,
                    remove_all_role_mappings)


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
        create_default_roles()
        annotator = User.objects.create_user(username=cls.annotator_name,
                                             password=cls.annotator_pass)
        approver = User.objects.create_user(username=cls.approver_name,
                                            password=cls.approver_pass)
        project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                 password=cls.project_admin_pass)
        project = mommy.make('TextClassificationProject', users=[annotator, approver, project_admin])
        cls.doc = mommy.make('Document', project=project)
        cls.url = reverse(viewname='approve_labels', args=[project.id, cls.doc.id])
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
