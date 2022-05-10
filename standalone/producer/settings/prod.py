import sys
from pathlib import Path
import codecs
import yaml
from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = False

PROJECT_ROOT = Path(__file__).abspath().dirname().dirname().dirname().dirname()
sys.path.append(PROJECT_ROOT)

with codecs.open(os.environ.get("MUX_CONFIG"), encoding='utf-8') as env_file:
    ENV = yaml.safe_load(env_file)

AWS_ACCESS_KEY_ID = ENV.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = ENV.get('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_ACL = ENV.get('AWS_DEFAULT_ACL')
AWS_QUERYSTRING_AUTH = ENV.get('AWS_QUERYSTRING_AUTH')
AWS_S3_CUSTOM_DOMAIN = ENV.get('AWS_S3_CUSTOM_DOMAIN')
AWS_S3_REGION_NAME = ENV.get('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = ENV.get('AWS_STORAGE_BUCKET_NAME')

SITE_NAME = ENV.get('SITE_NAME', SITE_NAME)
ALLOWED_HOSTS = [ENV.get("MUX_HOST", SITE_NAME)]

CACHES = ENV.get('CACHES', CACHES)

CORS_ORIGIN_ALLOW_ALL = ENV.get('CORS_ORIGIN_ALLOW_ALL', CORS_ORIGIN_ALLOW_ALL)
CORS_ORIGIN_WHITELIST = ENV.get('CORS_ORIGIN_WHITELIST', CORS_ORIGIN_WHITELIST)

CSRF_COOKIE_SECURE = ENV.get('CSRF_COOKIE_SECURE', CSRF_COOKIE_SECURE)
CSRF_TRUSTED_ORIGINS = ENV.get('CSRF_TRUSTED_ORIGINS', CSRF_TRUSTED_ORIGINS)

DATABASES = ENV.get('DATABASES', DATABASES)

DEFAULT_FILE_STORAGE = ENV.get('DEFAULT_FILE_STORAGE', DEFAULT_FILE_STORAGE)

MEDIA_URL = ENV.get('MEDIA_URL', MEDIA_URL)
MEDIA_ROOT = ENV.get('MEDIA_ROOT', MEDIA_ROOT)
MEDIA_STORAGE_BACKEND = ENV.get('MEDIA_STORAGE_BACKEND', MEDIA_STORAGE_BACKEND)

HUEY = ENV.get('HUEY', HUEY)

SECRET_KEY = ENV.get('SECRET_KEY', SECRET_KEY)

STATIC_ROOT = ENV.get('STATIC_ROOT', STATIC_ROOT)
STATICFILES_STORAGE = ENV.get('STATICFILES_STORAGE', STATICFILES_STORAGE)

if ENV.get('DISABLE_CLICKJACKING_MIDDLEWARE', DISABLE_CLICKJACKING_MIDDLEWARE):
    MIDDLEWARE.remove("django.middleware.clickjacking.XFrameOptionsMiddleware")

common_cache = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": "redis://redis:6379",
}

TIME_ZONE = ENV.get('TIME_ZONE', TIME_ZONE)

# Sentry.io integration
SENTRY_DSN = ENV.get('SENTRY_DSN')

if SENTRY_DSN:
    import sentry_sdk
    import subprocess
    from sentry_sdk.integrations.django import DjangoIntegration
    try:
        platform_git_commit = subprocess.check_output(['git', 'log', '--pretty=format:"%H"', '-n 1']).strip()
        if isinstance(platform_git_commit, bytes):
            platform_git_commit = platform_git_commit.decode('utf-8')
        platform_git_commit = platform_git_commit.replace('"', '')
    except (subprocess.CalledProcessError, OSError):
        platform_git_commit = ''
    sentry_sdk.init(
        SENTRY_DSN,
        auto_enabling_integrations=False,
        integrations=[DjangoIntegration()],
        environment=ENV.get('SENTRY_ENVIRONMENT', 'Unknown environment'),
        release=platform_git_commit,
        send_default_pii=True
    )
