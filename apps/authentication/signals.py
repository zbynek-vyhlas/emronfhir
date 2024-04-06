from allauth.account.models import EmailAddress
from django.dispatch import Signal, receiver

password_reset_signal = Signal()


@receiver(password_reset_signal)
def verify_email_used_for_password_reset(sender, **kwargs):
    """
    Unverified email set to verified if used to reset password.
    """
    user = kwargs.get("user")
    if user.email and not user.email_verified:
        email_obj, created = EmailAddress.objects.get_or_create(
            user=user, email=user.email, defaults={"verified": True}
        )
        if not created:
            email_obj.verified = True
            email_obj.save()
