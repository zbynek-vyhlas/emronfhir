import pytest
from django.urls import reverse
from rest_framework import status

from testing_resources.fixtures.scenarios.basic import clients, users  # noqa


@pytest.mark.django_db
class TestCSRFTokenAPI:
    def test_get_csrf_token(self, clients):
        for client_type in ["user1", "unauthenticated"]:
            response = clients[client_type].get(reverse("csrf"))
            assert response.status_code == status.HTTP_200_OK
            assert "csrftoken" in response.cookies
