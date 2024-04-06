from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@ensure_csrf_cookie
@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def set_csrf_token(request):
    return Response({"detail": "CSRF cookie set"})
