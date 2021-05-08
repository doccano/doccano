from rest_framework import status
from rest_framework.reverse import reverse

from .utils import CRUDMixin, make_tag, make_user, prepare_project


class TestTagList(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project()
        cls.non_member = make_user()
        make_tag(project=cls.project.item)
        cls.url = reverse(viewname='tag_list', args=[cls.project.item.id])

    def test_return_tags_to_member(self):
        for member in self.project.users:
            response = self.assert_fetch(member, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)

    def test_does_not_return_tags_to_non_member(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_does_not_return_tags_to_unauthenticated_user(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)


class TestTagCreate(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project()
        cls.non_member = make_user()
        cls.url = reverse(viewname='tag_list', args=[cls.project.item.id])
        cls.data = {'text': 'example'}

    def test_allow_admin_to_create_tag(self):
        response = self.assert_create(self.project.users[0], status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], self.data['text'])

    def test_disallow_non_admin_to_create_tag(self):
        for member in self.project.users[1:]:
            self.assert_create(member, status.HTTP_403_FORBIDDEN)

    def test_disallow_unauthenticated_user_to_create_tag(self):
        self.assert_create(expected=status.HTTP_403_FORBIDDEN)


class TestTagDelete(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project()
        cls.non_member = make_user()

    def setUp(self):
        tag = make_tag(project=self.project.item)
        self.url = reverse(viewname='tag_detail', args=[self.project.item.id, tag.id])

    def test_allow_admin_to_delete_tag(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)

    def test_disallow_non_admin_to_delete_tag(self):
        for member in self.project.users[1:]:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_disallow_unauthenticated_user_to_delete_tag(self):
        self.assert_delete(expected=status.HTTP_403_FORBIDDEN)
