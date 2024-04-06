import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status

from testing_resources.fixtures.scenarios.basic import clients, users  # noqa

faker = Faker()
User = get_user_model()


@pytest.mark.django_db
class TestSettingsAPI:
    USER_SCENARIOS = [
        ("unauthenticated", status.HTTP_401_UNAUTHORIZED, {}),
        ("acc_exp_refr_valid", status.HTTP_401_UNAUTHORIZED, {}),
        ("user1", status.HTTP_200_OK, {}),
        ("staff1", status.HTTP_200_OK, settings.DJANGO_ADMIN_PATH),
        ("superuser1", status.HTTP_200_OK, settings.DJANGO_ADMIN_PATH),
    ]

    @pytest.mark.parametrize(
        "user_type, expected_status, expected_data", USER_SCENARIOS
    )
    def test_get_settings(self, clients, user_type, expected_status, expected_data):
        """
        Testing the GET method of the Settings API endpoint for different user types
        """
        resp = clients[user_type].get(reverse("core:settings"))
        assert resp.status_code == expected_status
        assert resp.data.get("django_admin_path", {}) == expected_data


@pytest.mark.django_db
class TestUserAPI:
    @pytest.mark.parametrize("user_type", ["user1", "staff1", "superuser1"])
    def test_get_user(self, clients, user_type, users):
        user = users[user_type]
        data = {
            "pk": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "extra_data": user.extra_data,
        }
        resp = clients[user_type].get(reverse("core:user"))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == data

    def test_get_user_unauthenticated(self, clients):
        for client_type in ["unauthenticated", "acc_exp_refr_valid"]:
            resp = clients[client_type].get(reverse("core:user"))
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_patch_first_n_last_name(self, clients, users):
        user = users["user1"]
        data = {"first_name": faker.first_name(), "last_name": faker.last_name()}
        resp = clients["user1"].patch(reverse("core:user"), data=data)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["first_name"] == data["first_name"]
        assert resp.data["last_name"] == data["last_name"]
        assert User.objects.get(pk=user.pk).first_name == data["first_name"]
        assert User.objects.get(pk=user.pk).last_name == data["last_name"]
