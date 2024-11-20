from allauth.account.adapter import DefaultAccountAdapter
from ..itcoty_web.envs import load_config
# <<<<<<< HEAD
# from django.conf import settings
#
#
# class CustomAdapter(DefaultAccountAdapter):
#     def send_confirmation_mail(self, request, emailconfirmation, signup):
#         activate_url = f"https://4dev.itcoty.ru/api/v1/verify_email/{emailconfirmation.key}/"
#         context = {
#             "user": emailconfirmation.email_address.user,
#             "activate_url": activate_url,
#             "current_site": settings.SITE_NAME
#                    }
#         self.send_mail(
#             "account/email/email_confirmation_message",
#             emailconfirmation.email_address.email,
#             context,
#         )
# =======


env = load_config()


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Customizing a URL for the email confirmation."""

        url = super().get_email_confirmation_url(request, emailconfirmation)

        return url.replace("http://localhost", env.server.this)
