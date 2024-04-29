from collections.abc import Iterable

import pytest
import requests
from django.conf import LazySettings
from faker import Faker

from testlib.client import Client, RandomUser

fake: Faker = Faker("ru_RU")

default_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Safari",
}

host = "127.0.0.1"


@pytest.fixture(scope="function")
def client() -> Iterable[Client]:
    with requests.Session() as session:
        session.headers.update(default_headers)
        yield Client(host=f"http://{host}:8000", session=session)


@pytest.fixture(scope="function")
def random_user() -> RandomUser:
    email = fake.email()
    password = fake.password()
    return RandomUser(email, password)


@pytest.fixture(scope="function")
def override_email_backend(settings: LazySettings) -> None:
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
