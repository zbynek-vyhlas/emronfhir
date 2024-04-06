import celery
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import mail_admins, mail_managers
from django.utils.timezone import now


@celery.shared_task
def delete_notverified_email_users():
    User = get_user_model()
    # delete all users which have been created before PERIOD_TO_VERIFY_EMAIL and are not yet verified
    User.objects.annotate_email_verified().filter(
        created__lt=(now() - settings.PERIOD_TO_VERIFY_EMAIL),
        _email_verified=False,
        is_superuser=False,
    ).delete()


@celery.shared_task
def async_mail_admins(subject, body):
    mail_admins(subject, body)


@celery.shared_task
def async_mail_managers(subject, body):
    mail_managers(subject, body)
