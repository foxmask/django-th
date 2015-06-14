from __future__ import absolute_import

VERSION = (0, 10, 1)  # PEP 386
__version__ = ".".join([str(x) for x in VERSION])

default_app_config = 'django_th.apps.DjangoThConfig'

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
