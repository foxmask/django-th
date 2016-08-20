# coding: utf-8
from django.core import management

management.call_command('recycle', verbosity=0, interactive=False)
