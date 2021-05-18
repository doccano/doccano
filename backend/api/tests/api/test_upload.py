from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse

from ...models import DOCUMENT_CLASSIFICATION
from .utils import CRUDMixin, create_default_roles, make_user, prepare_project


class TestFeatures(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        create_default_roles()
        cls.user = make_user()
        cls.url = reverse('features')

    @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER=None)
    def test_no_cloud_upload(self):
        response = self.assert_fetch(self.user, status.HTTP_200_OK)
        self.assertFalse(response.json().get('cloud_upload'))


class TestImportCatalog(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.url = reverse(viewname='catalog', args=[self.project.item.id])

    def test_allows_project_admin_to_list_catalog(self):
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        for item in response.data:
            self.assertIn('name', item)

    def test_denies_non_project_admin_to_list_catalog(self):
        for member in self.project.users[1:]:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)
