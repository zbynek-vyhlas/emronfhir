from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("user/", views.UserView.as_view(), name="user"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
