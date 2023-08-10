from django.utils.http import urlencode
from rest_framework import status
from rest_framework.reverse import reverse

from .utils import make_assignment, make_doc, make_example_state
from api.tests.utils import CRUDMixin
from projects.models import ProjectType
from projects.tests.utils import prepare_project
from users.tests.utils import make_user


class TestExampleListAPI(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        self.example = make_doc(self.project.item)
        for member in self.project.members:
            make_assignment(self.project.item, self.example, member)
        self.data = {"text": "example"}
        self.url = reverse(viewname="example_list", args=[self.project.item.id])

    def test_allows_project_member_to_list_examples(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)
            self.assertIn("results", response.data)
            for item in response.data["results"]:
                self.assertIn("text", item)

    def test_denies_non_project_member_to_list_examples(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_list_examples(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_create_example(self):
        response = self.assert_create(self.project.admin, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], self.data["text"])

    def test_denies_non_admin_to_create_example(self):
        for member in self.project.staffs:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_create_example(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)

    def test_example_is_not_approved_if_another_user_approve_it(self):
        make_example_state(self.example, self.project.admin)
        response = self.assert_fetch(self.project.annotator, status.HTTP_200_OK)
        self.assertFalse(response.data["results"][0]["is_confirmed"])


class TestExampleListCollaborative(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION, collaborative_annotation=True)
        self.example = make_doc(self.project.item)
        for member in self.project.members:
            make_assignment(self.project.item, self.example, member)
        self.url = reverse(viewname="example_list", args=[self.project.item.id])

    def test_example_is_approved_if_someone_approve_it(self):
        admin = self.project.admin
        approver = self.project.approver

        make_example_state(self.example, admin)
        response = self.assert_fetch(admin, status.HTTP_200_OK)
        self.assertTrue(response.data["results"][0]["is_confirmed"])
        response = self.assert_fetch(approver, status.HTTP_200_OK)
        self.assertTrue(response.data["results"][0]["is_confirmed"])


class TestExampleListFilter(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        example1 = make_doc(self.project.item)
        example2 = make_doc(self.project.item)
        example3 = make_doc(self.project.item)
        for member in self.project.members:
            make_assignment(self.project.item, example1, member)
            make_assignment(self.project.item, example2, member)
            make_assignment(self.project.item, example3, member)
        make_example_state(example1, self.project.admin)

    def reverse(self, query_kwargs=None):
        base_url = reverse(viewname="example_list", args=[self.project.item.id])
        self.url = "{}?{}".format(base_url, urlencode(query_kwargs))

    def assert_filter(self, data, user, expected):
        self.reverse(query_kwargs=data)
        response = self.assert_fetch(user, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], expected)

    def test_returns_only_approved_examples(self):
        user = self.project.admin
        self.assert_filter(data={"confirmed": "True"}, user=user, expected=1)

    def test_returns_only_non_approved_examples(self):
        user = self.project.admin
        self.assert_filter(data={"confirmed": "False"}, user=user, expected=2)

    def test_returns_all_examples(self):
        user = self.project.admin
        self.assert_filter(data={"confirmed": ""}, user=user, expected=3)

    def test_does_not_return_approved_example_to_another_user(self):
        user = self.project.approver
        self.assert_filter(data={"confirmed": "True"}, user=user, expected=0)


class TestExampleDetail(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        example = make_doc(self.project.item)
        self.data = {"text": "example"}
        self.url = reverse(viewname="example_detail", args=[self.project.item.id, example.id])

    def test_allows_project_member_to_get_example(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertIn("text", response.data)

    def test_denies_non_project_member_to_get_example(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_example(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_update_example(self):
        response = self.assert_update(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.data["text"])

    def test_denies_non_admin_to_update_example(self):
        for member in self.project.staffs:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_example(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_delete_example(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)

    def test_denies_non_admin_to_delete_example(self):
        for member in self.project.staffs:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_example(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)
