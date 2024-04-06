import re
from unittest.mock import patch

import pytest
from allauth.account.models import EmailAddress
from authentication.signals import password_reset_signal
from authentication.views import OwnPasswordResetConfirmView
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from testing_resources.fixtures.scenarios.basic import clients, users  # noqa

User = get_user_model()


@pytest.mark.django_db
class TestPasswordResetSignal:
    @staticmethod
    def check_n_extract_mail_data(mail_body):
        username = re.search(r"\?username=(\w+)&", mail_body)
        uid = re.search(r"&uid=(\w+)&", mail_body)
        token = re.search(r"&token=([\w-]+)", mail_body)
        assert (
            username and uid and token
        ), "username, uid, and token must be included in the link"
        return uid.group(1), token.group(1)

    def test_password_reset_signal_called(self, client, users, mailoutbox):
        with patch("authentication.signals.password_reset_signal.send") as signal_mock:
            user = users["user1"]
            resp = client.post(reverse("request_password_reset"), {"email": user.email})
            assert resp.status_code == 200
            uid, token = self.check_n_extract_mail_data(mailoutbox[0].body)
            new_password = "some_New_Password321"
            data = {
                "uid": uid,
                "token": token,
                "new_password1": new_password,
                "new_password2": new_password,
            }
            resp = client.post(
                reverse("reset_password"),
                data,
            )
            assert resp.status_code == status.HTTP_200_OK
            assert signal_mock.call_count == 1
            assert signal_mock.call_args[1]["user"] == user
            assert signal_mock.call_args[1]["sender"] == OwnPasswordResetConfirmView

    @pytest.mark.parametrize(
        "email_exists",
        [True, False],
    )
    @pytest.mark.parametrize(
        "verified",
        [True, False],
    )
    def test_verify_email_used_for_password_reset_receiver(
        self, users, email_exists, verified
    ):
        # setup
        user = users["user1"]
        if email_exists:
            EmailAddress.objects.create(user=user, email=user.email, verified=verified)
        expected_count = 1 if email_exists else 0
        assert EmailAddress.objects.filter(user=user).count() == expected_count
        assert user.email_verified == (email_exists and verified)
        # testing
        password_reset_signal.send(sender="test", user=user)
        assert (
            EmailAddress.objects.filter(
                user=user, email=user.email, verified=True
            ).count()
            == 1
        )
        # Testing whether the email was also verified by the password reset
        # first invalidating the cached property by deleating the property, otherwise
        # it would stay cashed with the old value, even after using `.refresh_from_db()`.
        if hasattr(user, "email_verified"):
            delattr(user, "email_verified")
        assert user.email_verified
