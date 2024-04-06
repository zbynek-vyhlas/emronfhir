import re

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status

from testing_resources.fixtures.scenarios.basic import clients, users  # noqa

faker = Faker()
User = get_user_model()


@pytest.mark.django_db
class TestJWTTokenAPI:
    @pytest.mark.parametrize(
        "user_type, expected_access_valid, expected_refresh_valid",
        [
            ("unauthenticated", False, False),
            ("user1", True, True),
            ("acc_exp_refr_valid", False, True),
            ("acc_n_refr_expired", False, False),
        ],
    )
    def test_refreshing_access_token_api(
        self, clients, user_type, expected_access_valid, expected_refresh_valid
    ):
        resp = clients[user_type].get(reverse("core:user"))
        if expected_access_valid:
            assert resp.status_code == status.HTTP_200_OK
            for key in ["username", "email", "first_name", "last_name"]:
                assert key in resp.data
        else:
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED

        resp = clients[user_type].post(reverse("token_refresh"))
        if expected_refresh_valid:
            assert resp.status_code == status.HTTP_200_OK
            assert "access-token" in resp.cookies
        else:
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRegistrationAPI:
    @pytest.fixture
    def user(self):
        email = faker.email()
        username = faker.user_name()
        password = faker.password()
        data = {
            "email": email,
            "username": username,
            "password1": password,
            "password2": password,
        }
        return locals()

    def test_registration(self, mailoutbox, user, client):
        # setup
        assert User.objects.count() == 0
        assert len(mailoutbox) == 0

        # testing
        # `rest_register` url name can be found in dj_rest_auth.registration.urls
        resp = client.post(reverse("rest_register"), user["data"])
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data["detail"] == "Verification e-mail sent."
        assert User.objects.count() == 1
        u = User.objects.get()
        assert u.email == user["email"]
        assert u.username == user["username"]
        assert u.check_password(user["password"])
        assert not u.email_verified
        assert u.emailaddress_set.count() == 1
        assert len(mailoutbox) == 1
        mail_body = mailoutbox[0].body

        # test that link to confirm an email address is in the sent email
        url = reverse("url_in_confirmation_email", args=["key"]).rstrip("key/")
        escaped_url = url.replace("/", "\\/")
        match = re.search(escaped_url + r"\/[A-Za-z0-9_\-:]+\/", mail_body)
        assert (
            match
        ), "Link to confirm an email address not found in the sent email body."

        # test email will verify by clicking on the link
        url = match.group()
        resp = client.get(url)
        assert resp.status_code == status.HTTP_302_FOUND

        # invalidating the cached property by deleating the property, otherwise
        # it would stay cashed with the old value, even after using `.refresh_from_db()`.
        assert u.emailaddress_set.first().verified is True
        assert u.emailaddress_set.count() == 1
        if hasattr(u, "email_verified"):
            delattr(u, "email_verified")
        assert u.email_verified

    @pytest.mark.parametrize(
        "missing",
        [
            "email",
            "username",
            "password1",
            "password2",
        ],
    )
    def test_registration_missing_fields(self, mailoutbox, client, user, missing):
        # setup
        assert User.objects.count() == 0
        assert len(mailoutbox) == 0

        # creating data
        data = user["data"]
        data.pop(missing)

        # testing
        # `rest_register` url name can be found in dj_rest_auth.registration.urls
        resp = client.post(reverse("rest_register"), data)
        if missing == "username":
            assert resp.status_code == status.HTTP_201_CREATED
            assert User.objects.count() == 1
            assert len(mailoutbox) == 1
        else:
            assert resp.status_code == status.HTTP_400_BAD_REQUEST
            assert User.objects.count() == 0
            assert len(mailoutbox) == 0

    def test_registration_taken_username(self, mailoutbox, user, client):
        assert User.objects.count() == 0

        # create already existing user
        username1 = faker.user_name()
        email1 = faker.email()
        # make sure email of existing user is distinct from email of user to be created via API
        while email1 == user["email"]:
            email1 = faker.email()
        User.objects.create(email=email1, username=username1)
        assert User.objects.count() == 1

        # request to create a new user having the same username as the existing user
        new_user_data = user["data"]
        new_user_data["username"] = username1

        # `rest_register` url name can be found in dj_rest_auth.registration.urls
        resp = client.post(reverse("rest_register"), new_user_data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.count() == 1

        # check the existing user has not been modified
        u = User.objects.get()
        assert u.email == email1
        assert u.username == username1
        assert len(mailoutbox) == 0

    def test_registration_bad_data(self, mailoutbox, user, client):
        # setup
        assert User.objects.count() == 0

        # creating bad data
        bad_email_data = user["data"]
        bad_email_data["email"] = "not-email-structure"
        # make sure password1 != password2
        password2 = faker.password()
        while password2 == user["password"]:
            password2 = faker.password()
        not_matching_password_data = user["data"]
        not_matching_password_data["password2"] = password2
        bad_data = [bad_email_data, not_matching_password_data]

        # testing
        for data in bad_data:
            # `rest_register` url name can be found in dj_rest_auth.registration.urls
            resp = client.post(reverse("rest_register"), data)
            assert resp.status_code == status.HTTP_400_BAD_REQUEST
            assert User.objects.count() == 0
            assert len(mailoutbox) == 0


@pytest.mark.django_db
class TestPasswordResetAPI:
    @pytest.fixture
    def user(self, users):
        user = users["user1"]
        old_password = faker.password()
        user.set_password(old_password)
        user.save()
        return user, old_password

    @staticmethod
    def check_n_extract_mail_data(mail_body):
        assert (
            "/reset-your-password-here/" in mail_body
        ), "link to reset password not found in the sent email body"
        username = re.search(r"\?username=(\w+)&", mail_body)
        uid = re.search(r"&uid=(\w+)&", mail_body)
        token = re.search(r"&token=([\w-]+)", mail_body)
        assert (
            username and uid and token
        ), "username, uid, and token must be included in the link"
        return uid.group(1), token.group(1)

    @staticmethod
    def create_data(uid, token, new_password):
        return {
            "uid": uid,
            "token": token,
            "new_password1": new_password,
            "new_password2": new_password,
        }

    @staticmethod
    def assert_bad_request(resp, user, old_password):
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db()
        assert user.check_password(old_password)
        # Testing whether the email was also verified by the password reset
        # first invalidating the cached property by deleating the property, otherwise
        # it would stay cashed with the old value, even after using `.refresh_from_db()`.
        if hasattr(user, "email_verified"):
            delattr(user, "email_verified")
        assert not user.email_verified

    def test_password_reset(self, client, user, mailoutbox):
        # set up
        user, old_password = user
        assert not user.email_verified
        assert len(mailoutbox) == 0

        # testing request for password reset
        resp = client.post(reverse("request_password_reset"), {"email": user.email})
        assert resp.status_code == 200
        assert len(mailoutbox) == 1
        uid, token = self.check_n_extract_mail_data(mailoutbox[0].body)

        # testing resetting the password
        new_password = faker.password()
        # make sure new_password is distinct from old_password
        while new_password == old_password:
            new_password = faker.password()
        data = self.create_data(uid, token, new_password)
        resp = client.post(
            reverse("reset_password"),
            data,
        )
        assert resp.status_code == status.HTTP_200_OK
        assert len(mailoutbox) == 1, "there should be no new email sent"
        user.refresh_from_db()
        assert user.check_password(new_password)
        # Testing whether the email was also verified by the password reset
        # first invalidating the cached property by deleating the property, otherwise
        # it would stay cashed with the old value, even after using `.refresh_from_db()`.
        if hasattr(user, "email_verified"):
            delattr(user, "email_verified")
        assert user.email_verified

    @pytest.mark.parametrize(
        "missing",
        [
            "uid",
            "token",
            "new_password1",
            "new_password2",
        ],
    )
    def test_password_reset_missing_fields(self, client, user, mailoutbox, missing):
        # set up
        user, old_password = user
        assert not user.email_verified
        assert len(mailoutbox) == 0

        # testing request for password reset
        resp = client.post(reverse("request_password_reset"), {"email": user.email})
        assert resp.status_code == 200
        assert len(mailoutbox) == 1
        uid, token = self.check_n_extract_mail_data(mailoutbox[0].body)

        # testing resetting the password
        new_password = faker.password()
        # make sure new_password is distinct from old_password
        while new_password == old_password:
            new_password = faker.password()
        data = self.create_data(uid, token, new_password)
        data.pop(missing)
        resp = client.post(
            reverse("reset_password"),
            data,
        )
        self.assert_bad_request(resp, user, old_password)
        assert len(mailoutbox) == 1, "there should be no new email sent"

    def test_password_reset_bad_data(self, client, user, mailoutbox):
        """Testing password reset with new_password1 != new_password2"""
        # set up
        user, old_password = user
        assert not user.email_verified
        assert len(mailoutbox) == 0

        # testing request for password reset
        resp = client.post(reverse("request_password_reset"), {"email": user.email})
        assert resp.status_code == 200
        assert len(mailoutbox) == 1
        uid, token = self.check_n_extract_mail_data(mailoutbox[0].body)

        # testing resetting the password
        new_password1 = faker.password()
        new_password2 = faker.password()
        # make sure new_password1 is distinct from new_password2
        while new_password1 == new_password2:
            new_password2 = faker.password()
        data = self.create_data(uid, token, new_password1)
        data["new_password2"] = new_password2
        resp = client.post(
            reverse("reset_password"),
            data,
        )
        self.assert_bad_request(resp, user, old_password)
        assert len(mailoutbox) == 1, "there should be no new email sent"


@pytest.mark.django_db
class TestLogInAPI:
    @pytest.fixture
    def user_w_verified_email(self, users, request):
        user = users[request.param]
        password = faker.password()
        user.set_password(password)
        user.save()
        EmailAddress.objects.create(user=user, email=user.email, verified=True)
        assert user.email_verified
        return user, password

    @staticmethod
    def check_resp(resp):
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        for key in [
            "access",
            "refresh",
            "username",
            "email",
            "first_name",
            "last_name",
        ]:
            assert key not in resp.data

    @pytest.mark.parametrize(
        # `indirect=True` is instructing to use this parametrize to parametrize above created
        # user_w_verified_email fixture. The second argument here is sent as
        # `request` -> `request.param` parameter in the fixture.
        "user_w_verified_email",
        ["user1", "staff1", "superuser1"],
        indirect=True,
    )
    def test_login(self, user_w_verified_email, clients):
        # set up
        user, password = user_w_verified_email

        # testing
        resp = clients["unauthenticated"].post(
            reverse("rest_login"),
            {"email": user.email, "password": password},
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["access"]
        assert not resp.data["refresh"]
        for key in ["username", "email", "first_name", "last_name"]:
            assert getattr(user, key, "") == resp.data["user"].get(key)

    @pytest.mark.parametrize(
        "wrong",
        [
            [
                "email",
            ],
            [
                "password",
            ],
            ["email", "password"],
        ],
    )
    @pytest.mark.parametrize(
        # `indirect=True` is instructing to use this parametrize to parametrize above created
        # user_w_verified_email fixture. The second argument here is sent as
        # `request` -> `request.param` parameter in the fixture.
        "user_w_verified_email",
        ["user1", "staff1", "superuser1"],
        indirect=True,
    )
    def test_login_wrong_credentials(self, user_w_verified_email, clients, wrong):
        # set up
        user, password = user_w_verified_email
        # make sure wrong email and password are distinct from the correct ones
        wrong_email = faker.email()
        while wrong_email == user.email:
            wrong_email = faker.email()
        wrong_password = faker.password()
        while wrong_password == password:
            wrong_password = faker.password()

        # testing
        resp = clients["unauthenticated"].post(
            reverse("rest_login"),
            {
                "email": wrong_email if "email" in wrong else user.email,
                "password": wrong_password if "password" in wrong else password,
            },
        )
        self.check_resp(resp)

    @pytest.mark.parametrize(
        "missing",
        [
            [
                "email",
            ],
            [
                "password",
            ],
            ["email", "password"],
        ],
    )
    @pytest.mark.parametrize(
        # `indirect=True` is instructing to use this parametrize to parametrize above created
        # user_w_verified_email fixture. The second argument here is sent as
        # `request` -> `request.param` parameter in the fixture.
        "user_w_verified_email",
        ["user1", "staff1", "superuser1"],
        indirect=True,
    )
    def test_login_missing_fields(self, user_w_verified_email, clients, missing):
        # set up
        user, password = user_w_verified_email

        # testing
        resp = clients["unauthenticated"].post(
            reverse("rest_login"),
            {
                "email": "" if "email" in missing else user.email,
                "password": "" if "password" in missing else password,
            },
        )
        self.check_resp(resp)

    @pytest.mark.parametrize("user_type", ["user1", "staff1", "superuser1"])
    def test_login_notverified_email(self, users, user_type, clients):
        # set up
        user = users[user_type]
        password = faker.password()
        user.set_password(password)
        user.save()
        assert not EmailAddress.objects.filter(
            user=user, email=user.email, verified=True
        ).exists()
        assert not user.email_verified

        # testingd
        resp = clients["unauthenticated"].post(
            reverse("rest_login"),
            {"email": user.email, "password": password},
        )
        self.check_resp(resp)


@pytest.mark.django_db
class TestLogOutAPI:
    @pytest.mark.parametrize("user_type", ["user1", "staff1", "superuser1"])
    def test_logout(self, clients, user_type):
        client = clients[user_type]
        resp = client.get(reverse("core:user"))
        assert resp.status_code == status.HTTP_200_OK
        resp = client.post(reverse("rest_logout"))
        assert resp.status_code == status.HTTP_200_OK
        assert "Successfully logged out." in resp.data["detail"]
        # JWT are stateless, so even after logging out, the token is still valid until
        # it expires. Server doesn't invalidate these tokens.


@pytest.mark.django_db
class TestPasswordChangeAPI:
    @staticmethod
    def prepare_user(users):
        user = users["user1"]
        old_password = faker.password()
        new_password = faker.password()
        assert old_password != new_password
        user.set_password(old_password)
        user.save()
        return user, old_password, new_password

    def test_password_change(self, clients, users):
        # set up
        user, old_password, new_password = self.prepare_user(users)

        # testing
        resp = clients["user1"].post(
            reverse("password_change"),
            {
                "old_password": old_password,
                "new_password1": new_password,
                "new_password2": new_password,
            },
        )
        assert resp.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password(new_password)

    def test_password_change_unauthenticated(self, clients, users):
        # set up
        user, old_password, new_password = self.prepare_user(users)

        # testing
        for client_type in ["unauthenticated", "acc_exp_refr_valid"]:
            resp = clients[client_type].post(
                reverse("password_change"),
                {
                    "old_password": old_password,
                    "new_password1": new_password,
                    "new_password2": new_password,
                },
            )
            assert resp.status_code == status.HTTP_401_UNAUTHORIZED
            user.refresh_from_db()
            assert user.check_password(old_password)

    @pytest.mark.parametrize(
        "missing",
        [
            "old_password",
            "new_password1",
            "new_password2",
        ],
    )
    def test_password_change_missing_fields(self, clients, users, missing):
        # set up
        user, old_password, new_password = self.prepare_user(users)

        # testing
        data = {
            "old_password": old_password,
            "new_password1": new_password,
            "new_password2": new_password,
        }
        data.pop(missing)
        resp = clients["user1"].post(
            reverse("password_change"),
            data,
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        user.refresh_from_db()
        assert user.check_password(old_password)
