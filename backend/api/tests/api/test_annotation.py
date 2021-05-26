from rest_framework import status
from rest_framework.reverse import reverse

from ...models import DOCUMENT_CLASSIFICATION, Category
from .utils import (CRUDMixin, make_annotation, make_doc, make_label,
                    make_user, prepare_project)


class TestAnnotationList(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        cls.non_member = make_user()
        doc = make_doc(cls.project.item)
        for member in cls.project.users:
            make_annotation(task=DOCUMENT_CLASSIFICATION, doc=doc, user=member)
        cls.url = reverse(viewname='annotation_list', args=[cls.project.item.id, doc.id])

    def test_allows_project_member_to_fetch_annotation(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)  # fetch only own annotation

    def test_denies_non_project_member_to_fetch_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_fetch_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_bulk_delete_annotation(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)
        count = Category.objects.count()
        self.assertEqual(count, 2)  # delete only own annotation


class TestSharedAnnotationList(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(task=DOCUMENT_CLASSIFICATION, collaborative_annotation=True)
        doc = make_doc(cls.project.item)
        for member in cls.project.users:
            make_annotation(task=DOCUMENT_CLASSIFICATION, doc=doc, user=member)
        cls.url = reverse(viewname='annotation_list', args=[cls.project.item.id, doc.id])

    def test_allows_project_member_to_fetch_all_annotation(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 3)

    def test_allows_project_member_to_bulk_delete_annotation(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)
        count = Category.objects.count()
        self.assertEqual(count, 0)  # delete all annotation in the doc


class TestAnnotationCreation(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        label = make_label(self.project.item)
        self.data = {'label': label.id}
        self.url = reverse(viewname='annotation_list', args=[self.project.item.id, doc.id])

    def test_allows_project_member_to_annotate(self):
        for member in self.project.users:
            self.assert_create(member, status.HTTP_201_CREATED)

    def test_denies_non_project_member_to_annotate(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_annotate(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestAnnotationDetail(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        label = make_label(self.project.item)
        annotation = make_annotation(task=DOCUMENT_CLASSIFICATION, doc=doc, user=self.project.users[0])
        self.data = {'label': label.id}
        self.url = reverse(viewname='annotation_detail', args=[self.project.item.id, doc.id, annotation.id])

    def test_allows_owner_to_get_annotation(self):
        self.assert_fetch(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_owner_to_get_annotation(self):
        for member in self.project.users[1:]:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_get_annotation(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_annotation(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_owner_to_update_annotation(self):
        self.assert_update(self.project.users[0], status.HTTP_200_OK)

    def test_denies_non_owner_to_update_annotation(self):
        for member in self.project.users[1:]:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_annotation(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_owner_to_delete_annotation(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)

    def test_denies_non_owner_to_delete_annotation(self):
        for member in self.project.users[1:]:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_annotation(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)


class TestSharedAnnotationDetail(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION, collaborative_annotation=True)
        doc = make_doc(self.project.item)
        annotation = make_annotation(task=DOCUMENT_CLASSIFICATION, doc=doc, user=self.project.users[0])
        label = make_label(self.project.item)
        self.data = {'label': label.id}
        self.url = reverse(viewname='annotation_detail', args=[self.project.item.id, doc.id, annotation.id])

    def test_allows_any_member_to_get_annotation(self):
        for member in self.project.users:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_allows_any_member_to_update_annotation(self):
        for member in self.project.users:
            self.assert_update(member, status.HTTP_200_OK)

    def test_allows_any_member_to_delete_annotation(self):
        self.assert_delete(self.project.users[1], status.HTTP_204_NO_CONTENT)
