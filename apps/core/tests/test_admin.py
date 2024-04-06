from unittest.mock import patch

from django.urls import reverse


@patch("django.conf.settings.DJANGO_ADMIN_PATH", "test-admin/")
def test_reverse_admin():
    assert "/test-admin/" == reverse("admin:index")
