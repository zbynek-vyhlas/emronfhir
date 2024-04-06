import pytest
from allauth.account.models import EmailAddress
from core.fake_data import UserFactory
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    @pytest.mark.parametrize(
        ["hasattr_email_verified", "_email_verified", "email_verified1"],
        [
            [False, False, False],
            [False, True, False],
            [True, False, False],
            [True, True, True],
        ],
    )
    @pytest.mark.parametrize(
        ["has_email_address", "email_address_verified", "email_verified2"],
        [
            [False, True, False],
            [True, False, False],
            [True, True, True],
        ],
    )
    def test_email_verified(
        self,
        hasattr_email_verified,
        _email_verified,
        email_verified1,
        has_email_address,
        email_address_verified,
        email_verified2,
    ):
        """
        Test `email_verified` cached_property
        """
        user = UserFactory.create()
        if hasattr_email_verified:
            user._email_verified = _email_verified
            assert user.email_verified is email_verified1
        else:
            if has_email_address:
                EmailAddress.objects.create(
                    user=user, email=user.email, verified=email_address_verified
                )
            assert user.email_verified is email_verified2

    @pytest.mark.parametrize(
        ["verified", "user_email_verified"],
        [
            [False, False],
            [True, True],
        ],
    )
    def test_email_verification_case_mismatch(self, verified, user_email_verified):
        """
        Test that email is considered verified even when the letter case dont match
        """
        user = UserFactory.create()
        EmailAddress.objects.create(user=user, email=user.email, verified=verified)
        assert user.email_verified == user_email_verified
        # changing the case of the first letter in the email
        user.email = user.email.capitalize()
        user.save()
        # .email_verified is a cached property, we need new User instance
        user = User.objects.get(pk=user.pk)
        assert (
            user.email_verified == user_email_verified
        ), "email should be considered as verified even when letter case does not match"

    def test_annotate_email_verified(self):
        """
        Test that `annotate_email_verified` works
        """
        user = UserFactory.create()
        assert User.objects.count() == 1
        assert user.email_verified is False
        assert hasattr(self, "_email_verified") is False
        assert (
            user.__class__.objects.annotate_email_verified()
            .get(pk=user.pk)
            ._email_verified
            is False
        )
        EmailAddress.objects.create(user=user, email=user.email, verified=True)
        if hasattr(user, "email_verified"):
            delattr(user, "email_verified")
        assert user.email_verified is True
        assert hasattr(self, "_email_verified") is False
        assert (
            user.__class__.objects.annotate_email_verified()
            .get(pk=user.pk)
            ._email_verified
            is True
        )
