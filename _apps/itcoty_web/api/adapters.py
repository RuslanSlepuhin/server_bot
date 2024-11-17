from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = f"https://4dev.itcoty.ru/api/v1/verify_email/{emailconfirmation.key}/"
        context = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": settings.SITE_NAME
                   }
        self.send_mail(
            "account/email/email_confirmation_message",
            emailconfirmation.email_address.email,
            context,
        )