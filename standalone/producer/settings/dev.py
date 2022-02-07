from .base import *  # pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = True

# Make it easier to view the stacktrace in iframes by disabling x-frame protection
MIDDLEWARE.remove("django.middleware.clickjacking.XFrameOptionsMiddleware")

# Django debug toolbar
INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# More explicit LTI authentication logging
LOGGING["loggers"]["lti_toolbox"] = {  # type: ignore
    "handlers": ["console"],
    "level": "DEBUG",
    "propagate": False,
}
