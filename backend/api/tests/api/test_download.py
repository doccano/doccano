from rest_framework import status
from rest_framework.reverse import reverse

from ...models import DOCUMENT_CLASSIFICATION
from .utils import CRUDMixin, prepare_project


class TestDownloadCatalog(CRUDMixin):

    def setUp(self):
        self.project = prepare_project(task=DOCUMENT_CLASSIFICATION)
        self.url = reverse(viewname='download-format', args=[self.project.item.id])

    def test_allows_project_admin_to_list_catalog(self):
        response = self.assert_fetch(self.project.users[0], status.HTTP_200_OK)
        for item in response.data:
            self.assertIn('name', item)

    def test_denies_non_project_admin_to_list_catalog(self):
        for member in self.project.users[1:]:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)
