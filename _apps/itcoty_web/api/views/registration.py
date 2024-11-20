from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework.response import Response
from rest_framework import status


class CustomVerifyEmailView(VerifyEmailView):
    """Customize email verification using GET request."""

    def get(self, request, *args, **kwargs):
        """The GET request handling."""
        key = kwargs.get("key")
        if key:
            self.kwargs["key"] = key
            confirmation = self.get_object()
            confirmation.confirm(request)
            return Response(
                {"detail": "Email confirmed"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "Invalid key"},
            status=status.HTTP_400_BAD_REQUEST
        )
