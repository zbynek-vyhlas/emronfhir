from urllib.parse import urlparse

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import resolve


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # Creating custom email template for password reset email
        if template_prefix == "account/email/password_reset_key":
            # example of context["password_reset_url"] = 'https://127.0.0.1:8000/api/v1/auth/
            # not-used-url-but-has-to-be-here/3v/bzx5zy-585a0b72554ea329ad1dfb55192650e2/'
            url = urlparse(context["password_reset_url"])
            kwargs = resolve(url.path).kwargs
            uid = kwargs.get("uidb64")
            token = kwargs.get("token")
            # while in development frontend runs on different domain than backend so to
            # make this url work even in development, following is needed:
            domain = (
                settings.FRONTEND_DOMAIN if settings.FRONTEND_DOMAIN else url.netloc
            )
            context["domain"] = domain
            username = context["user"].username
            context["username"] = username
            context["reset_password_url"] = (
                f"{url.scheme}://{domain}/reset-your-password-here/?"
                f"username={username}&uid={uid}&token={token}"
            )
            context["password_reset_timeout_days"] = int(
                settings.PASSWORD_RESET_TIMEOUT / 60 / 60 / 24
            )
            message = self.render_mail(
                "account/email/password_reset_key", email, context
            )
            message.send()
        else:
            super().send_mail(template_prefix, email, context)
