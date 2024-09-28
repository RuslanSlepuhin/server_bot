from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoConfig:
    secret_key: str
    su_username: str
    su_password: str


@dataclass
class PostrgresConfig:
    name: str
    host: str
    port: int
    username: str
    password: str

@dataclass
class Config:
    django: DjangoConfig
    postgres: PostrgresConfig


def load_config() -> Config:
    env: Env = Env()
    env.read_env("./.env")

    return Config(
        django=DjangoConfig(
            secret_key=env.str("DJANGO_SECRET_KEY"),
            su_username=env.str("DJANGO_SU_USERNAME"),
            su_password=env.str("DJANGO_SU_PASSWORD"),
        ),
        postgres=PostgresConfig()
    )


