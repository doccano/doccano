from rest_framework import status
from rest_framework.reverse import reverse

from ...models import DOCUMENT_CLASSIFICATION
from .utils import CRUDMixin, make_image, make_user, prepare_project


class TestImageListAPI(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        make_image(self.project.item)
        self.url = reverse(viewname='image_list', args=[self.project.item.id])

    def test_allows_project_member_to_list_images(self):
        for member in self.project.users:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_denies_non_project_member_to_list_images(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_list_images(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)


class TestImageDetail(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.non_member = make_user()
        image = make_image(self.project.item)
        self.url = reverse(viewname='image_detail', args=[self.project.item.id, image.id])

    def test_allows_project_member_to_get_image(self):
        for member in self.project.users:
            self.assert_fetch(member, status.HTTP_200_OK)

    def test_denies_non_project_member_to_get_image(self):
        self.assert_fetch(self.non_member, status.HTTP_403_FORBIDDEN)

    def test_denies_unauthenticated_user_to_get_image(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)

    def test_allows_project_admin_to_delete_image(self):
        self.assert_delete(self.project.users[0], status.HTTP_204_NO_CONTENT)

    def test_denies_non_project_admin_to_delete_image(self):
        for member in self.project.users[1:]:
            self.assert_delete(member, status.HTTP_403_FORBIDDEN)

    def test_denies_non_project_member_to_delete_image(self):
        self.assert_delete(self.non_member, status.HTTP_403_FORBIDDEN)
