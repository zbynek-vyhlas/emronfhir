from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Exists, OuterRef
from django.utils.functional import cached_property
from django.utils.timezone import now


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserQuerySet(models.QuerySet):
    def annotate_email_verified(self):
        verified_email_addresses = EmailAddress.objects.filter(
            user=OuterRef("pk"), verified=True
        )
        return self.annotate(_email_verified=Exists(verified_email_addresses))


class TheUserManager(UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def annotate_email_verified(self):
        return self.get_queryset().annotate_email_verified()


class User(CreatedUpdatedMixin, AbstractUser):
    extra_data = models.JSONField(
        default=dict, help_text="extra data about the user", blank=True
    )
    objects = TheUserManager()

    def __str__(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.email

    @cached_property
    def email_verified(self):
        if hasattr(self, "_email_verified"):
            return self._email_verified
        else:
            try:
                # get user email address querying allauth
                email_address: EmailAddress = self.emailaddress_set.get(
                    email__iexact=self.email
                )
                return email_address.verified
            except EmailAddress.DoesNotExist:
                return False
