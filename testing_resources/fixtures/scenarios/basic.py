from datetime import timedelta

import pytest
from core.fake_data import UserFactory
from django.conf import settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def users():
    user1 = UserFactory.create(username="user1", is_staff=False, is_superuser=False)
    user2 = UserFactory.create(username="user2", is_staff=False, is_superuser=False)

    staff1 = UserFactory.create(username="staff1", is_staff=True, is_superuser=False)
    superuser1 = UserFactory.create(
        username="superuser1", is_staff=False, is_superuser=True
    )
    return locals()


def expire_token(token):
    token_validity_period = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
    token.set_exp(
        from_time=timezone.now() - token_validity_period - timedelta(seconds=2),
        lifetime=token_validity_period,
    )
    with pytest.raises(TokenError):
        # check that the access token has really expired
        token.check_exp()
    return token


def create_auth_client(user, expire_access=False, expire_refresh=False) -> APIClient:
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    refresh_token.check_exp()
    access_token.check_exp()
    if expire_access:
        access_token = expire_token(access_token)
    if expire_refresh:
        refresh_token = expire_token(refresh_token)
    client = APIClient()
    client.cookies["access-token"] = str(access_token)
    # access token can also be passed in the Authorization header:
    # auth_headder = settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0]
    # client.credentials(HTTP_AUTHORIZATION=f"{auth_headder} {str(access_token)}")
    # ..however I prefer to use only the http only cookies and
    # not use the Authorization header at all
    client.cookies["refresh-token"] = str(refresh_token)
    return client


@pytest.fixture
def clients(users):
    # If I want use any fixture in test, I need to import all the fixtures separately: the one I
    # want to use as well as all the fixtures on which its dependant. Or just use `import *`.
    unauthenticated = APIClient()

    user1 = create_auth_client(users["user1"])
    user2 = create_auth_client(users["user2"])

    staff1 = create_auth_client(users["staff1"])
    superuser1 = create_auth_client(users["superuser1"])

    acc_exp_refr_valid = create_auth_client(users["user1"], expire_access=True)
    acc_n_refr_expired = create_auth_client(
        users["user1"], expire_access=True, expire_refresh=True
    )
    del users
    return locals()
