from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Customizing an URL for the email confirmation."""

        url = super().get_email_confirmation_url(request, emailconfirmation)

        return url.replace("localhost", "4dev.itcoty.ru")