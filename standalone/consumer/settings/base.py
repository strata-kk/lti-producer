import os
import typing as t

SECRET_KEY = "set-me"
DEBUG = True
ALLOWED_HOSTS: t.List[str] = []
ROOT_URLCONF = "urls"

INSTALLED_APPS = [
    "django.contrib.staticfiles",
]
STATIC_URL = "static/"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(os.path.dirname(__file__), "..", "templates")],
        "APP_DIRS": True,
    },
]

# LTI consumer parameters
LTI_KEY = "set-me"
LTI_SECRET = "set-me"
LTI_LAUNCH_URL = "http://localhost:9630/lti/1.1/launch"
LTI_EXTRA_PARAMETERS: t.Dict[str, str] = {}
LTI_CONTEXT_ID = "dummy context id"
LTI_CONTEXT_TITLE = "dummy title"
LTI_LOCALE = "en"
LTI_USER_ID = "userid123"
LTI_USER_EMAIL = f"{LTI_USER_ID}@example.com"
LTI_RESOURCE_LINK_ID = "test-id"
LTI_ROLE = "Student"  # Student/Instructor
