import os
from os.path import abspath, dirname
from sys import path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")

WSGI_ROOT = dirname(abspath(__file__))
path.append(WSGI_ROOT)

application = get_wsgi_application()
