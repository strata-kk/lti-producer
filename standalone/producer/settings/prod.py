from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = False

ALLOWED_HOSTS = [os.environ["MUX_HOST"]]

common_cache = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": "redis://redis:6379",
}
CACHES = {
    "default": common_cache,
    "lti_replay": common_cache,
    "lti_apps": common_cache,
}

HUEY = {
    "huey_class": "huey.RedisHuey",
    "url": "redis://redis:6379",
    "immediate": False,
}

DATABASES = {
    "default": {
        "NAME": "ltiproducer",
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "postgresql",
    }
}
