from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.api.utils import (CRUDMixin, create_default_roles, make_user)


class TestRoleAPI(CRUDMixin):

    @classmethod
    def setUpTestData(cls):
        create_default_roles()
        cls.user = make_user()
        cls.url = reverse(viewname='roles')

    def test_allows_authenticated_user_to_get_roles(self):
        self.assert_fetch(self.user, status.HTTP_200_OK)

    def test_disallows_unauthenticated_user_to_get_roles(self):
        self.assert_fetch(expected=status.HTTP_403_FORBIDDEN)
