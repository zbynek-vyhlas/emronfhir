from dj_rest_auth.views import PasswordResetConfirmView

from .signals import password_reset_signal


class OwnPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Extended `PasswordResetConfirmView` to emit successful password reset signal
    """

    def post(self, request, *args, **kwargs):
        """
        extended to insert the `password_reset_signal`
        """

        # Serialization is also performed in the parent method; however,
        # we repeat the process to access the user instance required for the signal emission.
        # Additionally, it's necessary to conduct the serialization prior to invoking
        # super().post since the token's validity expires after full processing,
        # which would lead to failed validation.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()  # populates serializer.user
        response = super().post(request, *args, **kwargs)
        password_reset_signal.send(
            sender=self.__class__, request=request, user=serializer.user
        )
        return response
