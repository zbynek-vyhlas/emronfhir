from django.contrib.admin import site
from django.contrib.admin.apps import AdminConfig


class CustomAdminConfig(AdminConfig):
    # AdminConfig inherits from AppConfig
    default_site = "apps.admin.custom_admin.CustomAdminSite"

    def ready(self):
        # This method is called once Django has loaded all models, making it
        # a suitable place to unregister models from the admin.

        super().ready()
        from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
        from django.contrib.sites.models import Site

        # from django.contrib.auth.models import Group
        from rest_framework.authtoken.admin import TokenProxy

        # app Site
        site.unregister(Site)  # Site

        # app Social Account
        site.unregister(SocialAccount)  # Social application
        site.unregister(SocialToken)  # Social application token
        site.unregister(SocialApp)  # Social account

        # app Authentication and Authorization
        # site.unregister(Group) # Group

        # app Auth Token
        site.unregister(TokenProxy)  # Token
