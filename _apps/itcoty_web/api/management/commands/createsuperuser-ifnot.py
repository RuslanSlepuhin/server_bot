from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from itcoty_web.envs import load_config

User = get_user_model()
env = load_config()

class Command(BaseCommand):
    """
    Handle a superuser creating.
    """

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Checks if a superuser exists.
        If not, creates a superuser
        using credentials from .env file.
        """
        username = env.django.su_username
        password = env.django.su_password
        email = env.django.su_email

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' exists.")
            return

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' has been created.")
            return
