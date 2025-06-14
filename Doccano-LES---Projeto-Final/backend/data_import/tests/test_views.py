from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.utils import CRUDMixin
from projects.models import ProjectType
from projects.tests.utils import prepare_project


class TestImportCatalog(CRUDMixin):
    def setUp(self):
        self.project = prepare_project(task=ProjectType.DOCUMENT_CLASSIFICATION)
        self.url = reverse(viewname="catalog", args=[self.project.item.id])

    def test_allows_project_admin_to_list_catalog(self):
        response = self.assert_fetch(self.project.admin, status.HTTP_200_OK)
        for item in response.data:
            self.assertIn("name", item)

    def test_denies_project_staff_to_list_catalog(self):
        for member in self.project.staffs:
            self.assert_fetch(member, status.HTTP_403_FORBIDDEN)
