from unittest.mock import patch
from urllib.parse import urlparse

import pytest
from authentication.account import CustomAccountAdapter
from core.fake_data import UserFactory
from django.conf import settings
from django.urls import resolve, reverse
from faker import Faker

from testing_resources.fixtures.scenarios.basic import clients, users  # noqa

fake = Faker()


@pytest.mark.django_db
class TestCustomAccountAdapter:
    @pytest.mark.parametrize(
        "template_prefix",
        ["account/email/password_reset_key", "account/email/email_confirmation_signup"],
    )
    @pytest.mark.parametrize("frontend_domain", ["frontend-test.com", None])
    @pytest.mark.parametrize("passwor_reset_timeout", [86400, 54548])
    def test_send_mail(
        self, mailoutbox, frontend_domain, passwor_reset_timeout, template_prefix
    ):
        # setup
        template_prefix = template_prefix
        email = fake.email()
        user = UserFactory.create(
            username=fake.simple_profile()["username"], email=email
        )
        uid = fake.uuid4()
        token = fake.uuid4()
        netloc = fake.domain_name()
        context = {
            "password_reset_url": f"https://{netloc}/api/v1/auth/not-used-url-but-has-to-be-here/"
            f"{uid}/{token}/",
            "user": user,
        }

        # testing
        with patch.object(settings, "FRONTEND_DOMAIN", frontend_domain), patch.object(
            settings, "PASSWORD_RESET_TIMEOUT", passwor_reset_timeout
        ):
            CustomAccountAdapter().send_mail(template_prefix, email, context)
            assert len(mailoutbox) == 1
            domain = settings.FRONTEND_DOMAIN if settings.FRONTEND_DOMAIN else netloc
            pswd_timeout_in_days = int(settings.PASSWORD_RESET_TIMEOUT / 60 / 60 / 24)
            content_text = (
                "You're receiving this email because you or someone else has requested a "
                "password reset for your user account.",
                "Click the link below to reset your password.",
                f"https://{domain}/reset-your-password-here/?username="
                f"{user.username}&uid={uid}&token={token}",
                f"The link will be valid for {pswd_timeout_in_days} days.",
            )
            for item in content_text:
                if template_prefix == "account/email/password_reset_key":
                    assert item in mailoutbox[0].body
                else:
                    assert item not in mailoutbox[0].body

    @pytest.mark.parametrize("frontend_domain", ["http://frontend-test.com", None])
    @patch("authentication.account.CustomAccountAdapter.render_mail")
    # above created mock is always passed as a second parameter bellow
    def test_render_mail(self, mock_render_mail, frontend_domain, client):
        user = UserFactory.create(
            username=fake.simple_profile()["username"], email=fake.email()
        )
        with patch.object(settings, "FRONTEND_DOMAIN", frontend_domain), patch.object(
            settings, "PASSWORD_RESET_TIMEOUT", 86400  # 1 day in seconds
        ):
            client.post(reverse("request_password_reset"), {"email": user.email})
            mock_render_mail.assert_called_once()
            called_args = mock_render_mail.call_args[0]

            # check first and second argument in called mock_render_mail
            assert called_args[0] == "account/email/password_reset_key"
            assert called_args[1] == user.email

            # check third argument `context` in called mock_render_mail
            url = urlparse(called_args[2]["password_reset_url"])
            kwargs = resolve(url.path).kwargs
            uid = kwargs.get("uidb64")
            token = kwargs.get("token")
            domain = (
                settings.FRONTEND_DOMAIN if settings.FRONTEND_DOMAIN else "testserver"
            )
            context = {
                "domain": domain,
                "username": user.username,
                "reset_password_url": (
                    f"{url.scheme}://{domain}/reset-your-password-here/?"
                    f"username={user.username}&uid={uid}&token={token}"
                ),
                "password_reset_timeout_days": 1,
            }
            for key, value in context.items():
                assert key in called_args[2] and called_args[2][key] == value
