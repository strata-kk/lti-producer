import os
import typing as t
from pathlib import Path
from distutils.util import strtobool

# root folder: standalone/producer folder
BASE_DIR = Path(__file__).parent.parent.resolve()

SECRET_KEY = os.environ.get("MUX_DJANGO_SECRET_KEY", "setme")

DEBUG = True

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ["127.0.0.1", "localhost"]

ENABLE_CLICKJACKING_MIDDLEWARE = strtobool(os.environ.get("ENABLE_CLICKJACKING_MIDDLEWARE", "True"))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "huey.contrib.djhuey",
    "lti_toolbox",
    "ltiproducer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

if ENABLE_CLICKJACKING_MIDDLEWARE:
    MIDDLEWARE.append("django.middleware.clickjacking.XFrameOptionsMiddleware")

AUTHENTICATION_BACKENDS = [
    "lti_toolbox.backend.LTIBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "urls"

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
        },
    },
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {},
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

WSGI_APPLICATION = "wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Caching
# LTI applications should use the "lti_apps" cache and prefix all keys with a
# "myltiapp:" namespace.
common_cache = {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
CACHES = {
    "default": common_cache,
    "lti_replay": common_cache,
    "lti_apps": common_cache,
}

# Asynchronous tasks
# https://huey.readthedocs.io/en/latest/django.html#setting-things-up
HUEY = {
    "huey_class": "huey.SqliteHuey",
    "filename": BASE_DIR / "huey.sqlite3",
    "immediate": False,
}

# LTI-specific settings
LTI_APP_NAME_KEY = "custom_app"
LTI_PRODUCER_URLS: t.Dict[str, str] = {}
LTI_LAUNCH_VIEWS: t.Dict[str, str] = {}
