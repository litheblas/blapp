from os import path

from django.conf import global_settings as DEFAULT
from django.urls import reverse_lazy

from blapp.utils.settings import PrefixEnv

ENV_PREFIX = "BLAPP_"
env = PrefixEnv(prefix=ENV_PREFIX)

# Build paths inside the project like this: path.join(REPO_ROOT, ...)
REPO_ROOT = path.dirname(path.dirname(path.abspath(__file__)))
APP_ROOT = path.join(REPO_ROOT, "blapp")

TEST_MODE = env.bool("TEST_MODE", default=False)
DEBUG = env.bool("DEBUG_MODE", default=False)
SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST", default=[])
CORS_ALLOW_CREDENTIALS = True

# Only sets SECURE_PROXY_SSL_HEADER if explicitly defined. The format of
# BLAPP_SECURE_PROXY_HEADER is <header>=<value>, where <value> is the value of
# the HTTP header <header> set by the proxy on secure (i.e. HTTPS) requests.
# Example value: HTTP_X_FORWARDED_PROTO=https
# Read https://docs.djangoproject.com/en/1.11/ref/settings/#secure-proxy-ssl-header
_SECURE_PROXY_SSL_HEADER = env.str("SECURE_PROXY_HEADER", default=None)
SECURE_PROXY_SSL_HEADER = (
    tuple(_SECURE_PROXY_SSL_HEADER.split("=", 1)) if _SECURE_PROXY_SSL_HEADER else None
)

DATABASES = {"default": env.db("DATABASE_URL"), "legacy": env.db("LEGACY_DATABASE_URL")}

if env.str("TEST_DATABASE_URL", default=""):
    DATABASES["default"]["TEST"] = env.db("TEST_DATABASE_URL")

DATABASE_ROUTERS = ("blapp.legacy.db_routers.LegacyRouter",)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

INSTALLED_APPS = [
    # First to override runserver
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "django_extensions",
    "graphene_django",
    "mptt",
    "oidc_provider",
    "oauth2_provider",
    "widget_tweaks",
    "blapp.api",
    "blapp.auth",
    "blapp.commerce",
    "blapp.frontend",
    "blapp.legacy",
    "blapp.people",
    "blapp.utils",
    "blapp.events",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ROOT_URLCONF = "blapp.urls"
ASGI_APPLICATION = "blapp.routing.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    }
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
PASSWORD_HASHERS = DEFAULT.PASSWORD_HASHERS + [
    # For compatibility with passwords from legacy database
    "django.contrib.auth.hashers.UnsaltedMD5PasswordHasher"
]
AUTH_USER_MODEL = "blapp_auth.UserAccount"
AUTHENTICATION_BACKENDS = [
    "oauth2_provider.backends.OAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
    "blapp.auth.backends.ServiceAccountTokenBackend",
]
LOGIN_URL = reverse_lazy("login")

OIDC_USERINFO = "blapp.auth.oidc.user_info"
OIDC_EXTRA_SCOPE_CLAIMS = "blapp.auth.oidc.CustomScopeClaims"
OIDC_TEMPLATES = {
    "authorize": "registration/openid-authorize.html",
    "error": "registration/openid-error.html",
}

OAUTH2_PROVIDER = {
#    'OIDC_ENABLED': True,
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
   },
    'PKCE_REQUIRED': True,
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = path.join(REPO_ROOT, ".var", "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# Files in this directory will be served from the web root. favicon.ico is a
# good use case for this.
WHITENOISE_ROOT = path.join(APP_ROOT, "utils", "root_static")

FRONTEND_SETTINGS = {"API_ROOT": reverse_lazy("api-graphql")}

SHELL_PLUS_MODEL_ALIASES = {"legacy": {"Person": "LegacyPerson"}}
