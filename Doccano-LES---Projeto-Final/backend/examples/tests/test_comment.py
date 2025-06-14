from rest_framework import status
from rest_framework.reverse import reverse

from .utils import make_comment, make_doc
from api.tests.utils import CRUDMixin
from projects.tests.utils import prepare_project
from users.tests.utils import make_user


class TestCommentListDocAPI(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project()
        cls.non_member = make_user()
        doc1 = make_doc(cls.project.item)
        doc2 = make_doc(cls.project.item)
        make_comment(doc1, cls.project.admin)
        make_comment(doc2, cls.project.admin)
        cls.data = {"text": "example"}
        cls.url = reverse(viewname="comment_list", args=[cls.project.item.id])
        cls.url += f"?example={doc1.id}"

    def test_allows_project_member_to_list_comments(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

    def test_denies_non_project_member_to_list_comments(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_list_comments(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_member_to_create_comment(self):
        for member in self.project.members:
            self.assert_create(member, status.HTTP_201_CREATED)

    def test_denies_non_project_member_to_create_comment(self):
        self.assert_create(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_create_comment(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestCommentListProjectAPI(CRUDMixin):
    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        self.doc = make_doc(self.project.item)
        make_comment(self.doc, self.project.admin)
        self.url = reverse(viewname="comment_list", args=[self.project.item.id])

    def test_allows_project_member_to_list_comments(self):
        for member in self.project.members:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(response.data["count"], 1)

    def test_denies_non_project_member_to_list_comments(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_list_comments(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def assert_bulk_delete(self, user=None, expected=status.HTTP_403_FORBIDDEN):
        ids = [item.id for item in self.doc.comments.all()]
        if user:
            self.client.force_login(user)
        response = self.client.delete(self.url, data={"ids": ids}, format="json")
        self.assertEqual(response.status_code, expected)

    def test_allows_project_member_to_delete_comments(self):
        # Todo: Disallow non admin to delete comments.
        for member in self.project.members:
            self.assert_bulk_delete(member, status.HTTP_204_NO_CONTENT)
            response = self.client.get(self.url)
            self.assertEqual(response.data["count"], 0)

    def test_denies_non_project_member_to_delete_comments(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_delete_comments(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)


class TestCommentDetailAPI(CRUDMixin):
    def setUp(self):
        self.project = prepare_project()
        self.non_member = make_user()
        doc = make_doc(self.project.item)
        comment = make_comment(doc, self.project.admin)
        self.data = {"text": "example"}
        self.url = reverse(viewname="comment_detail", args=[self.project.item.id, comment.id])

    def test_allows_comment_owner_to_get_comment(self):
        # Todo: Allows project member to get comment.
        self.assert_fetch(self.project.admin, status.HTTP_200_OK)

    def test_denies_non_comment_owner_to_get_comment(self):
        for member in self.project.staffs:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_get_comment(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_comment(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_comment_owner_to_update_comment(self):
        response = self.assert_update(self.project.admin, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], self.data["text"])

    def test_denies_non_comment_owner_to_update_comment(self):
        for member in self.project.staffs:
            self.assert_update(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_update_comment(self):
        self.assert_update(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_update_comment(self):
        self.assert_update(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_comment_owner_to_delete_comment(self):
        self.assert_delete(self.project.admin, status.HTTP_204_NO_CONTENT)

    def test_denies_non_comment_owner_to_delete_comment(self):
        for member in self.project.staffs:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_comment(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_delete_comment(self):
        self.assert_delete(expected=status.HTTP_403_FORBIDDEN)
