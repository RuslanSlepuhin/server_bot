from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoConfig:
    secret_key: str
    su_username: str
    su_password: str
    su_email: str
    debug: bool


@dataclass
class DevDatabaseConfig:
    name: str
    host: str
    port: int
    user: str
    password: str
    default: str
    version: int
    winpath: str


@dataclass
class ServerConfig:
    dev4: str
    prod: str
    localhost: str
    notymail: str


@dataclass
class EmailConfig:
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_sender: str
    smtp_theme: str


@dataclass
class Config:
    django: DjangoConfig
    database: DevDatabaseConfig
    server: ServerConfig
    email: EmailConfig


def load_config() -> Config:
    env: Env = Env()
    env.read_env("./.env")
    return Config(
        django=DjangoConfig(
            secret_key=env.str("DJANGO_SECRET_KEY"),
            su_username=env.str("DJANGO_SU_USERNAME"),
            su_password=env.str("DJANGO_SU_PASSWORD"),
            su_email=env.str("DJANGO_SU_EMAIL"),
            debug=env.bool("DJANGO_DEBUG"),
        ),
        database=DevDatabaseConfig(
            name=env.str("DEV_DB_NAME"),
            host=env.str("DEV_DB_HOST"),
            port=env.int("DEV_DB_PORT"),
            user=env.str("DEV_DB_USER"),
            password=env.str("DEV_DB_PASSWORD"),
            default=env.str("DEFAULT_DB_NAME"),
            version=env.int("LOCAL_DB_VERSION"),
            winpath=env.str("WINDOWS_DB_PATH"),
        ),
        server=ServerConfig(
            dev4=env.str("DEV_4SERVER"),
            prod=env.str("PROD_SERVER"),
            localhost=env.str("LOCALHOST"),
            notymail=env.str("NOTIFICATION_EMAIL"),
        ),
        email=EmailConfig(
            smtp_host=env.str("EMAIL_SMTP_HOST"),
            smtp_port=env.int("EMAIL_SMTP_PORT"),
            smtp_user=env.str("EMAIL_SMTP_USER"),
            smtp_password=env.str("EMAIL_SMTP_PASSWORD"),
            smtp_sender=env.str("EMAIL_DEFAULT_SENDER"),
            smtp_theme=env.str("EMAIL_DEFAULT_THEME"),
        ),

    )
