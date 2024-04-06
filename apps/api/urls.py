from django.urls import include, path

from . import views

urlpatterns = [
    path("csrf/", views.set_csrf_token, name="csrf"),
    path("", include("authentication.urls")),
    path("", include("core.urls", namespace="core")),
]
