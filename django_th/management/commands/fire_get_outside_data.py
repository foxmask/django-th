#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.utils.log import getLogger

from django_th.tasks import get_outside_cache

# create logger
logger = getLogger('django_th.trigger_happy')


class Command(BaseCommand):

    help = 'Trigger all data from cache in version 2'

    def handle(self, *args, **options):
        """
            get all the triggers that need to be handled
        """
        get_outside_cache.delay()
