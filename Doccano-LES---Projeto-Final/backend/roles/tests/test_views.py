from rest_framework import status
from rest_framework.reverse import reverse

from .utils import create_default_roles
from api.tests.utils import CRUDMixin
from users.tests.utils import make_user


class TestRoleAPI(CRUDMixin):
    @classmethod
    def setUpTestData(cls):
        create_default_roles()
        cls.user = make_user()
        cls.url = reverse(viewname="roles")

    def test_allows_authenticated_user_to_get_roles(self):
        self.assert_fetch(self.user, status.HTTP_200_OK)

    def test_denies_unauthenticated_user_to_get_roles(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)
