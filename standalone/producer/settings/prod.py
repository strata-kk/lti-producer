import yaml
import codecs
import sys
from path import Path as path
import pkg_resources

from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = False

ALLOWED_HOSTS = [os.environ.get("MUX_HOST", "localhost")]

PROJECT_ROOT = path(__file__).abspath().dirname().dirname().dirname().dirname()
sys.path.append(PROJECT_ROOT)

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

# override settings from YAML file defined in MUX_CONFIG environment variable

if os.environ.get("MUX_CONFIG", None):
    with codecs.open(os.environ.get("MUX_CONFIG"), encoding='utf-8') as f:
        vars().update(yaml.safe_load(f))

# https://github.com/strata-kk/mux-videos-lti-producer

try:
    pkg_resources.get_distribution("mux_lti_producer")
except pkg_resources.DistributionNotFound:
    pass
else:
    INSTALLED_APPS.append("muxltiproducer")

    LTI_PRODUCER_URLS = {
        "mux": "muxltiproducer.urls",
    }
    LTI_LAUNCH_VIEWS = {
        "mux": "mux:launch",
    }
    if not 'mux_signing_key' in sys.argv:
        if not "MUX_ENABLE_SIGNED_PLAYBACK" in vars() or MUX_ENABLE_SIGNED_PLAYBACK == True:
            if not "MUX_SIGNING_KEY_ID" in vars() or MUX_SIGNING_KEY_ID == "":
                raise NameError("MUX_ENABLE_SIGNED_PLAYBACK enabled but MUX_SIGNING_KEY_ID settings does not declared in configuration")
            if not "MUX_SIGNING_PRIVATE_KEY" in vars() or MUX_SIGNING_PRIVATE_KEY == "":
                raise NameError("MUX_ENABLE_SIGNED_PLAYBACK enabled but MUX_SIGNING_PRIVATE_KEY settings does not declared in configuration")

# Disable X-Frame-Options header to allow to launch LTI in iFrame
if not ENABLE_CLICKJACKING_MIDDLEWARE:
    MIDDLEWARE.remove("django.middleware.clickjacking.XFrameOptionsMiddleware")

# Sentry.io integration

if 'SENTRY_DSN' in vars() and SENTRY_DSN != '':
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
            environment=SENTRY_ENVIRONMENT if 'SENTRY_ENVIRONMENT' in vars() else 'unknown environment',
            release=platform_git_commit,
            send_default_pii=True
            )
