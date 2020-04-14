import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

WSGI_APPLICATION = 'config.wsgi.production.application'

sentry_sdk.init(
    dsn=SECRETS['dsn'],
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
# STATICFILES_DIRS = [
#     STATIC_ROOT
# ]
