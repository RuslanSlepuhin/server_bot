from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoConfig:
    secret_key: str
    su_username: str
    su_password: str
    debug: bool


@dataclass
class DevDatabaseConfig:
    name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class ServerConfig:
    dev4: str
    prod: str
    localhost: str


@dataclass
class Config:
    django: DjangoConfig
    database: DevDatabaseConfig
    server: ServerConfig


def load_config() -> Config:
    env: Env = Env()
    env.read_env("./.env")

    return Config(
        django=DjangoConfig(
            secret_key=env.str("DJANGO_SECRET_KEY"),
            su_username=env.str("DJANGO_SU_USERNAME"),
            su_password=env.str("DJANGO_SU_PASSWORD"),
            debug=env.bool("DJANGO_DEBUG"),
        ),
        database=DevDatabaseConfig(
            name=env.str("DEV_DB_NAME"),
            host=env.str("DEV_DB_HOST"),
            port=env.int("DEV_DB_PORT"),
            user=env.str("DEV_DB_USER"),
            password=env.str("DEV_DB_PASSWORD"),
        ),
        server=ServerConfig(
            dev4=env.str("DEV_4SERVER"),
            prod=env.str("PROD_SERVER"),
            localhost=env.str("LOCALHOST"),
        ),
    )
