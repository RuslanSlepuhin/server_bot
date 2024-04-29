from dataclasses import dataclass
from http import HTTPStatus

import orjson
import requests


@dataclass
class RandomUser:
    email: str
    password: str


@dataclass
class Client:
    host: str
    session: requests.Session

    def register(
        self,
        *,
        password: str,
        email: str,
    ) -> dict:
        response = self.session.post(
            f"{self.host}/api/v1/registration/",
            data=orjson.dumps(
                {
                    "password1": password,
                    "password2": password,
                    "email": email,
                }
            ),
        )
        assert response.status_code == HTTPStatus.CREATED, response.text
        return response.json()

    def activate(
        self,
        *,
        key: str,
    ) -> dict:
        response = self.session.post(
            f"{self.host}/api/v1/registration/verify-email/",
            data=orjson.dumps(
                {
                    "key": key,
                }
            ),
        )
        assert response.status_code == HTTPStatus.OK, response.text
        return response.json()

    def authenticate(
        self,
        *,
        password: str,
        username: str,
    ) -> dict:
        response = self.session.post(
            f"{self.host}/api/v1/login/",
            data={
                "password": password,
                "username": username,
            },
        )
        assert response.ok, response.text

        return response.json()
