# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

# django
from django.core.cache import caches

from logging import getLogger

cache = caches['django_th']
logger = getLogger('django_th.trigger_happy')


def recycle():
    """
        the purpose of this tasks is to recycle the data from the cache
        with version=2 in the main cache
    """
    # http://niwinz.github.io/django-redis/latest/#_scan_delete_keys_in_bulk
    for service in cache.iter_keys('th_*'):
        try:
            # get the value from the cache version=2
            service_value = cache.get(service, version=2)
            # put it in the version=1
            cache.set(service, service_value)
            # remote version=2
            cache.delete_pattern(service, version=2)
        except ValueError:
            pass
    logger.info('recycle of cache done!')
