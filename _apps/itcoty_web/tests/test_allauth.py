import re

from django.core import mail

from testlib.client import Client, RandomUser

# def test_registration(*,
#                       random_user: RandomUser,
#                       client: Client,
#                       override_email_backend: None,
#                       ) -> None:
#     response = client.register(email=random_user.email, password=random_user.password)
#     assert response == {"detail": "Verification e-mail sent."}
#
#     email_content = mail.outbox
#     token_regex = r"registration\/account-confirm-email\/([A-Za-z0-9:\-]+)\/"
#     match = re.search(token_regex, email_content)
#     assert match.groups(), "Could not find the token in the email"
#     token = match.group(1)
#
#     response = client.activate(key=token)
#     assert response == {"detail": "ok"}
