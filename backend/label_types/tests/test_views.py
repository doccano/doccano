import os

from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .utils import make_label
from api.tests.utils import CRUDMixin
from projects.models import ProjectType
from projects.tests.utils import make_project, prepare_project
from users.tests.utils import make_user

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestLabelList(CRUDMixin):
    def setUp(self):
        self.non_member = make_user()
        self.project_a = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION)
        self.label = make_label(self.project_a.item)
        self.url = reverse(viewname="category_types", args=[self.project_a.item.id])

        # Ensure that the API does not return the labels of the other project.
        self.project_b = make_project(task="Any", users=["admin"], roles=[settings.ROLE_PROJECT_ADMIN])
        make_label(self.project_b.item)

        # for label creation
        self.data = {"text": "example"}

    def test_returns_labels_to_project_member(self):
        for member in self.project_a.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], self.label.id)

    def test_does_not_return_labels_to_non_project_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_labels_to_unauthenticated_user(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_create_label(self):
        self.assert_create(self.project_a.admin, status.HTTP_201_CREATED)

    def test_denies_project_staff_to_create_label(self):
        for member in self.project_a.staffs:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_create_label(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_create_label(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_bulk_delete_label(self):
        self.assert_delete(self.project_a.admin, status.HTTP_204_NO_CONTENT, data={"ids": [self.label.id]})

    def test_denies_project_staff_to_bulk_delete_label(self):
        member = self.project_a.staffs[0]
        self.assert_delete(member, status.HTTP_403_FORBIDDEN, data={"ids": [self.label.id]})


class TestAllowMemberToCreateLabelType(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION, allow_member_to_create_label_type=True)
        cls.label = make_label(cls.project.item)
        cls.url = reverse(viewname="category_types", args=[cls.project.item.id])
        cls.data = {"text": "example"}

    def test_allows_member_to_create_label_type(self):
        for member in self.project.members:
            self.data["text"] = member.username
            self.assert_create(member, status.HTTP_201_CREATED)

    def test_denies_project_staff_to_bulk_delete_label(self):
        member = self.project.staffs[0]
        self.assert_delete(member, status.HTTP_403_FORBIDDEN, data={"ids": [self.label.id]})


class TestLabelDetailAPI(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user()
        cls.project = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION)
        cls.label = make_label(cls.project.item)
        cls.url = reverse(viewname="category_type", args=[cls.project.item.id, cls.label.id])
        cls.data = {"text": "example"}

    def test_returns_label_to_project_member(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["id"], self.label.id)

    def test_does_not_return_label_to_non_project_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_label_to_unauthenticated_user(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_update_label(self):
        response = self.assert_update(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.data["text"])

    def test_denies_project_staff_to_update_label(self):
        for member in self.project.staffs:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_label(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_update_label(self):
        self.assert_update(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_admin_to_delete_label(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)

    def test_denies_project_staff_to_delete_label(self):
        for member in self.project.staffs:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_label(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_delete_label(self):
        self.assert_delete(expected=status.HTTP_403_FORBIDDEN)


class TestLabelUploadAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.non_member = make_user()
        cls.project = prepare_project(ProjectType.DOCUMENT_CLASSIFICATION)
        cls.url = reverse(viewname="category_type_upload", args=[cls.project.item.id])

    def assert_upload_file(self, filename, user=None, expected_status=status.HTTP_403_FORBIDDEN):
        if user:
            self.client.force_login(user)
        with open(os.path.join(DATA_DIR, filename), "rb") as f:
            response = self.client.post(self.url, data={"file": f})
        self.assertEqual(response.status_code, expected_status)

    def test_allows_project_admin_to_upload_label(self):
        self.assert_upload_file("valid_labels.json", self.project.admin, status.HTTP_201_CREATED)

    def test_denies_project_member_to_upload_label(self):
        for member in self.project.staffs:
            self.assert_upload_file("valid_labels.json", member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_upload_label(self):
        self.assert_upload_file("valid_labels.json", self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_upload_label(self):
        self.assert_upload_file("valid_labels.json", expected_status=status.HTTP_403_FORBIDDEN)

    def test_try_to_upload_invalid_file(self):
        self.assert_upload_file("invalid_labels.json", self.project.admin, status.HTTP_400_BAD_REQUEST)
