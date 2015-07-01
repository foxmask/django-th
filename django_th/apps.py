from __future__ import absolute_import
from django.apps import AppConfig

from .celery import app as celery_app

class DjangoThConfig(AppConfig):
    name = 'django_th'
    verbose_name = "Trigger Happy"
