from rest_framework import status
from rest_framework.reverse import reverse

from ...models import DOCUMENT_CLASSIFICATION
from .utils import CRUDMixin, make_doc, make_user, prepare_project


class TestDocumentListAPI(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        make_doc(self.project.item)
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


class TestDocumentDetail(CRUDMixin):

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
