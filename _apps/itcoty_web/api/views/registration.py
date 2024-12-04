from django.http import JsonResponse
from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework.response import Response
from rest_framework import status
from itcoty_web.envs import load_config

env = load_config()

class CustomVerifyEmailView(VerifyEmailView):
    """Customize email verification using GET request."""

    def get(self, request, *args, **kwargs):
        """The GET request handling."""
        key = kwargs.get("key")
        if key:
            self.kwargs["key"] = key
            confirmation = self.get_object()
            confirmation.confirm(request)
            response = JsonResponse(
                {"detail": "Email confirmed"},
                status=status.HTTP_200_OK
            )
            response["Location"] = f"{env.server.this}/authorization"
            response.status_code = 302

            return response

        return Response(
            {"detail": "Invalid key"},
            status=status.HTTP_400_BAD_REQUEST
        )
