from django.conf import settings
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.reverse import reverse

from ...models import DOCUMENT_CLASSIFICATION
from .utils import (CRUDMixin, assign_user_to_role, make_doc,
                    make_example_state, make_user, prepare_project)


class TestExampleListAPI(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        self.example = make_doc(self.project.item)
        self.data = {'text': 'example'}
        self.url = reverse(viewname='example_list', args=[self.project.item.id])

    def test_allows_project_member_to_list_docs(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data['count'], 1)
            self.assertIn('results', response.data)
            for item in response.data['results']:
                self.assertIn('text', item)

    def test_denies_non_project_member_to_list_docs(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_list_docs(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_create_doc(self):
        response = self.assert_create(self.project.users[0], status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_denies_non_project_admin_to_create_doc(self):
        for member in self.project.users[1:]:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_create_doc(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)

    def test_is_confirmed(self):
        make_example_state(self.example, self.project.users[0])
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['is_confirmed'])

    def test_is_not_confirmed(self):
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        self.assertFalse(response.data['results'][0]['is_confirmed'])

    def test_does_not_share_another_user_confirmed(self):
        make_example_state(self.example, self.project.users[0])
        response = self.assert_fetch(self.project.users[1], status.HTTP_200_OK)
        self.assertFalse(response.data['results'][0]['is_confirmed'])


class TestExampleListCollaborative(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.example = make_doc(self.project.item)
        self.url = reverse(viewname='example_list', args=[self.project.item.id])

    def test_shares_confirmed_in_same_role(self):
        annotator1 = make_user()
        assign_user_to_role(annotator1, self.project.item, settings.ROLE_ANNOTATOR)
        annotator2 = make_user()
        assign_user_to_role(annotator2, self.project.item, settings.ROLE_ANNOTATOR)

        make_example_state(self.example, annotator1)
        response = self.assert_fetch(annotator1, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['is_confirmed'])
        response = self.assert_fetch(annotator2, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['is_confirmed'])

    def test_does_not_share_confirmed_in_other_role(self):
        admin = self.project.users[0]
        approver = self.project.users[1]

        make_example_state(self.example, admin)
        response = self.assert_fetch(admin, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['is_confirmed'])
        response = self.assert_fetch(approver, status.HTTP_200_OK)
        self.assertFalse(response.data['results'][0]['is_confirmed'])


class TestExampleListFilter(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.example = make_doc(self.project.item)
        make_example_state(self.example, self.project.users[0])

    def reverse(self, query_kwargs=None):
        base_url = reverse(viewname='example_list', args=[self.project.item.id])
        self.url = '{}?{}'.format(base_url, urlencode(query_kwargs))

    def assert_filter(self, data, user, expected):
        self.reverse(query_kwargs=data)
        response = self.assert_fetch(user, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], expected)

    def test_returns_example_if_confirmed_is_true(self):
        user = self.project.users[0]
        self.assert_filter(data={'confirmed': 'True'}, user=user, expected=1)

    def test_does_not_return_example_if_confirmed_is_false(self):
        user = self.project.users[0]
        self.assert_filter(data={'confirmed': 'False'}, user=user, expected=0)

    def test_returns_example_if_confirmed_is_empty(self):
        user = self.project.users[0]
        self.assert_filter(data={'confirmed': ''}, user=user, expected=1)

    def test_does_not_return_example_if_user_is_different(self):
        user = self.project.users[1]
        self.assert_filter(data={'confirmed': 'True'}, user=user, expected=0)

    def test_returns_example_if_user_is_different(self):
        user = self.project.users[1]
        self.assert_filter(data={'confirmed': 'False'}, user=user, expected=1)

    def test_returns_example_if_user_is_different_and_confirmed_is_empty(self):
        user = self.project.users[1]
        self.assert_filter(data={'confirmed': ''}, user=user, expected=1)


class TestExampleDetail(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        self.data = {'text': 'example'}
        self.url = reverse(viewname='example_detail', args=[self.project.item.id, doc.id])

    def test_allows_project_member_to_get_doc(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertIn('text', response.data)

    def test_denies_non_project_member_to_get_doc(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_doc(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_update_doc(self):
        response = self.assert_update(self.project.users[0], status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_denies_non_project_admin_to_update_doc(self):
        for member in self.project.users[1:]:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_doc(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_delete_doc(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)

    def test_denies_non_project_admin_to_delete_doc(self):
        for member in self.project.users[1:]:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_doc(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)


class TestApproveLabelsAPI(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        self.url = reverse(viewname='approve_labels', args=[self.project.item.id, doc.id])

    def test_allow_project_admin_and_approver_to_approve_and_disapprove(self):
        for member in self.project.users[:2]:
            self.data = {'approved': True}
            response = self.assert_create(member, status.HTTP_200_OK)
            self.assertEqual(response.data['annotation_approver'], member.username)
            self.data = {'approved': False}
            response = self.assert_create(member, status.HTTP_200_OK)
            self.assertIsNone(response.data['annotation_approver'])

    def test_denies_annotator_to_approve_and_disapprove(self):
        self.assert_create(self.project.users[2], status.HTTP_403_FORBIDDEN)
