# coding: utf-8
from django.core import management

management.call_command('recycle', verbosity=0, interactive=False)
management.call_command('read', verbosity=0, interactive=False)
management.call_command('publish', verbosity=0, interactive=False)
