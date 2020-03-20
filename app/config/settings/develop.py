from .base import *

DEBUG = True

INSTALLED_APPS += [
    'django_extensions',
]

WSGI_APPLICATION = 'config.wsgi.develop.application'
