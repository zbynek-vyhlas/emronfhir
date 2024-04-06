from datetime import timedelta
from unittest.mock import patch

import pytest
from allauth.account.models import EmailAddress
from core.fake_data import UserFactory
from core.tasks import (
    async_mail_admins,
    async_mail_managers,
    delete_notverified_email_users,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from faker import Faker

faker = Faker()

User = get_user_model()


@pytest.mark.django_db
class TestUserTasks:
    @pytest.mark.parametrize("is_active", [True, False])
    @pytest.mark.parametrize("is_staff", [True, False])
    @pytest.mark.parametrize("is_superuser", [True, False])
    @pytest.mark.parametrize("email_verified", [True, False])
    @pytest.mark.parametrize("add_timedelta", [timedelta(days=1), timedelta(days=-1)])
    def test_delete_notverified_email_users(
        self, settings, add_timedelta, email_verified, is_superuser, is_staff, is_active
    ):
        user = UserFactory.create(
            created=(now() - settings.PERIOD_TO_VERIFY_EMAIL + add_timedelta),
            is_superuser=is_superuser,
            is_active=is_active,
            is_staff=is_staff,
        )
        EmailAddress.objects.create(
            verified=email_verified, user=user, email=user.email
        )
        assert User.objects.count() == 1
        delete_notverified_email_users()
        if email_verified or add_timedelta > timedelta(days=0) or is_superuser:
            assert User.objects.count() == 1
        else:
            assert User.objects.count() == 0


@pytest.mark.django_db
class TestSendingEmails:
    @staticmethod
    def check_sent_email(mailoutbox, subject, body, recipients):
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        to = {email for name, email in recipients}
        assert set(mail.to) == to
        assert mail.subject == "Test prefix" + subject
        assert mail.body == body

    @patch("django.conf.settings.EMAIL_SUBJECT_PREFIX", "Test prefix")
    def test_async_mail_admins(self, mailoutbox):
        subject = faker.sentence()
        body = faker.text()
        assert len(mailoutbox) == 0
        async_mail_admins(subject, body)
        self.check_sent_email(mailoutbox, subject, body, settings.ADMINS)

    @patch("django.conf.settings.EMAIL_SUBJECT_PREFIX", "Test prefix")
    def test_async_mail_managers(self, mailoutbox):
        subject = faker.sentence()
        body = faker.text()
        assert len(mailoutbox) == 0
        async_mail_managers(subject, body)
        self.check_sent_email(mailoutbox, subject, body, settings.MANAGERS)
