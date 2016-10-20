# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

# django
from django.conf import settings
from django.core.cache import caches
from django.utils.log import getLogger

# trigger happy
from django_th.my_services import MyService

logger = getLogger('django_th.trigger_happy')


def recycle():
    """
        the purpose of this tasks is to recycle the data from the cache
        with version=2 in the main cache
    """
    logger = getLogger('django_th.trigger_happy')
    all_packages = MyService.all_packages()
    for package in all_packages:
        if package in settings.DJANGO_TH.get('services_wo_cache'):
            continue
        cache = caches[package]
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
