"""Django settings for itcoty_web project."""

from corsheaders.defaults import default_headers

from .envs import load_config
from .dirs import BASE_DIR, STATIC_DIR

env = load_config()
debug = env.django.debug


URL_VACANCY_TO_TG = (
    f"{env.server.localhost}:9000/api/v1/vacancy_to_tg/"
    if debug
    else f"{env.server.dev4}/api/v1/vacancy_to_tg/"
)

URL_USER_REQUEST = (
    f"{env.server.localhost}:9000/api/v1/users_requests/"
    if debug
    else f'{env.server.dev4}/api/v1/users_requests/'
)

SECRET_KEY = env.django.secret_key

DEBUG = True

ALLOWED_HOSTS = [
    'itcoty_web.backend',
    'localhost', '127.0.0.1',
    '4dev.itcoty.ru',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:9000',
    env.server.dev4,
    env.server.prod,
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "access-control-allow-credentials",
    "access-control-allow-headers",
    "access-control-allow-methods",
    "access-control-allow-origin",
    ]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:9000',
    env.server.dev4,
]

CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = "api.User"

SITE_ID = 1

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "api",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth.registration",
    "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "itcoty_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "itcoty_web" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "itcoty_web.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.database.name,
        "USER": env.database.user,
        "PASSWORD": env.database.password,
        "HOST": env.database.host,
        "PORT": env.database.port,
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = STATIC_DIR

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 1000,
    "PAGE_SIZE_QUERY_PARAM": "page_size",
    "MAX_PAGE_SIZE": 10000,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "JWT_AUTH_COOKIE": "access_token",
    "JWT_AUTH_REFRESH_COOKIE": "refresh_token",
    "REGISTER_SERIALIZER": "api.serializers.RegisterSerializer",
    "PASSWORD_RESET_SERIALIZER":
        "api.serializers.CustomPasswordResetSerializer",
    "UNIQUE_EMAIL": True,
    "OLD_PASSWORD_FIELD_ENABLED": True,
}

ACCOUNT_ADAPTER = "api.adapters.CustomAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = env.server.this
LOGIN_ON_EMAIL_CONFIRMATION = True


GOOGLE_REDIRECT_URL = "http://127.0.0.1:8000/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.email.smtp_host
EMAIL_HOST_USER = env.email.smtp_user
EMAIL_HOST_PASSWORD = env.email.smtp_password
EMAIL_PORT = env.email.smtp_port
EMAIL_USE_TLS = True

SERVER_EMAIL = env.server.notymail
DEFAULT_FROM_EMAIL = env.server.notymail

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
