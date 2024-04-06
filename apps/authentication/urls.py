from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordChangeView, PasswordResetView
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # REGISTRATION
    # needed for situations when user goes to expired email confirmation url
    path("accounts/", include("allauth.urls")),
    # more on this endpoint:
    # https://github.com/iMerica/dj-rest-auth/blob/master/dj_rest_auth/registration/urls.py
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    # more on this endpoint:
    # https://github.com/iMerica/dj-rest-auth/blob/master/dj_rest_auth/registration/urls.py
    # https://dj-rest-auth.readthedocs.io/en/latest/faq.html
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
    # This endpoint matches the link sent by email to confirm the email address,
    # after GET request to this endpoint (clicking on the link) the ConfirmEmailView confirms the
    # email (attribute `verified` of the EmailAddress instance linked to the User gets
    # value `True`).
    # This endpoint has to be registered before "auth/registration/" endpoint
    path(
        "auth/registration/account-confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
        name="url_in_confirmation_email",
    ),
    # endpoint for requesting a user registration
    path(
        "auth/registration/", include("dj_rest_auth.registration.urls")
    ),  # name="rest_register"
    # PASSWORD RESET
    # endpoint for requesting a password reset and
    # receiving email with link defined in CustomAccountAdapter
    # -> send a POST request with the user's email address
    path(
        "auth/request-password-reset/",
        PasswordResetView.as_view(),
        name="request_password_reset",
    ),
    # endpoint to wich a new password should be sent
    # -> send a POST request with data: new password1, password2, uid and token
    path(
        "auth/reset-password/",
        views.OwnPasswordResetConfirmView.as_view(),
        name="reset_password",
    ),
    # according to documentation (https://dj-rest-auth.readthedocs.io/en/latest/faq.html)
    # this url name `password_reset_confirm` is necessary
    # according to sourcecode
    # (https://github.com/iMerica/dj-rest-auth/blob/master/demo/demo/urls.py),
    # this url is used to generate email content
    # there has to be url called `password_reset_confirm` and there has to be
    # url taking 2 arguments: uidb64 and token eventhough it is not used.
    # In my CustomAccountAdapter I extract data from this url which is there provided in
    # context["password_reset_url"]
    path(
        "auth/not-used-url-but-has-to-be-here/<uidb64>/<token>/",
        TemplateView.as_view(),
        name="password_reset_confirm",
    ),
    # PASSWORD CHANGE
    path("auth/password/change/", PasswordChangeView.as_view(), name="password_change"),
    # OTHER
    # login, logout
    path("auth/", include("dj_rest_auth.urls")),
]
