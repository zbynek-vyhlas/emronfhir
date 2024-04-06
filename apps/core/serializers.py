from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "pk",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "extra_data",
        )
