from django.conf import settings
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # get_queryset() would expect URL keyword argument named `pk` to
        # create queryset and thereby identify the object, but thanks to JWT I already have
        # user in the request so I can perform self.request.user

        # `self.request.user` doesn't merely contain user data from the request itself,
        # it actually does several steps under the hood: extracting the user's ID from JWT,
        # then retrieving the corresponding user record from the database similar to
        # performing User.objects.get(id=user_id)), attaching this data to request object so
        # the self.request.user refers to this user object freshly retreived from database.
        return self.request.user


class SettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = {}
        if self.request.user.is_staff or self.request.user.is_superuser:
            response["django_admin_path"] = settings.DJANGO_ADMIN_PATH
        return Response(response)
