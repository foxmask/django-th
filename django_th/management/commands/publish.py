#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from multiprocessing import Pool, TimeoutError
# django
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.log import getLogger
# trigger happy
from django_th.models import TriggerService
from django_th.publish import publishing

# create logger
logger = getLogger('django_th.trigger_happy')


class Command(BaseCommand):

    help = 'Trigger all the services and '\
           'publish the data coming from the cache'

    def handle(self, *args, **options):
        """
            get all the triggers that need to be handled
        """
        from django.db import connection
        connection.close()
        trigger = TriggerService.objects.filter(
            status=True,
            user__is_active=True
        ).select_related('consumer__name', 'provider__name')

        try:
            with Pool(processes=settings.DJANGO_TH.get('processes')) as pool:
                result = pool.map_async(publishing, trigger)
                result.get(timeout=360)
        except TimeoutError as e:
            logger.warn(e)
