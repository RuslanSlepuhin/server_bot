from allauth.account.adapter import DefaultAccountAdapter
from ..itcoty_web.envs import load_config


env = load_config()


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Customizing a URL for the email confirmation."""

        url = super().get_email_confirmation_url(request, emailconfirmation)

        return url.replace("http://localhost", env.server.this)
