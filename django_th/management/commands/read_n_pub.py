#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from multiprocessing import Pool, TimeoutError
# django
from django.core.management.base import BaseCommand
from django.utils.log import getLogger
from django.core.cache import caches
# trigger happy
from django_th.models import TriggerService
from django_th.read import Read
from django_th.publish import Pub

# create logger
logger = getLogger('django_th.trigger_happy')
cache = caches['django_th']


class Command(BaseCommand):

    help = 'Fire only ONE trigger'

    def add_arguments(self, parser):
        parser.add_argument('--trigger_id', dest='trigger_id',
                            help='the trigger id to fire')

    def handle(self, *args, **options):
        """
            get the trigger to fire
        """
        trigger_id = options.get('trigger_id')
        trigger = TriggerService.objects.filter(
            id=int(trigger_id),
            status=True,
            user__is_active=True,
        ).select_related('consumer__name', 'provider__name')
        try:
            with Pool(processes=1) as pool:
                r = Read()
                result = pool.map_async(r.reading, trigger)
                result.get(timeout=360)
                p = Pub()
                result = pool.map_async(p.publishing, trigger)
                result.get(timeout=360)

                cache.delete('django_th' + '_fire_trigger_' + str(trigger_id))
        except TimeoutError as e:
            logger.warn(e)
