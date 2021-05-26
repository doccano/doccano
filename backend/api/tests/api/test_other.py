from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestHealthEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(viewname='health')

    def test_returns_green_status_on_health_endpoint(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['status'], 'green')
