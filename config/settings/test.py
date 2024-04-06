from .base import *  # noqa

DJANGO_ADMIN_PATH = "test-admin/"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


ADMINS = [
    ("Jenny Leny", "jennyleny@example.com"),
    ("Barbe Farbe", "barbefarbe@example.com"),
]
MANAGERS = [("John Doe", "johnDoe@example.com"), ("Bob Joe", "bobjoe@example.com")]
