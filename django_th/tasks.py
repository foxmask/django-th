# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow

# django
from django.conf import settings
from django.core.cache import caches
from django.utils.log import getLogger
from django.core.exceptions import ObjectDoesNotExist

# trigger happy
from django_th.services import default_provider
from django_th.models import TriggerService
from django_th.my_services import MyService

# create logger
logger = getLogger('django_th.trigger_happy')


default_provider.load_services()


def update_trigger(service):
    """
        update the date when occurs the trigger
        :param service: service object to update
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format(
        'YYYY-MM-DD HH:mm:ssZZ')
    TriggerService.objects.filter(id=service.id).update(date_triggered=now)


def log_update(service, to_update, status, count):
    """
        lets log everything at the end
        :param service: service object
        :param to_update: boolean to check if we have to update
        :param status: is everything worked fine ?
        :param count: number of data to update
        :type service: service object
        :type to_update: boolean
        :type status: boolean
        :type count: interger
    """
    if to_update:
        if status:
            logger.info("{} - {} new data".format(service, count))
        else:
            logger.warn("{} AN ERROR OCCURS ".format(service))
    else:
        logger.debug("{} nothing new ".format(service))


def reading(service):
    """
       get the data from the service and put theme in cache
       :param service: service object to read
       :type service: object
    """
    data = ()
    # flag to know if we have to update
    to_update = False
    # flag to get the status of a service
    status = False
    count_new_data = 0
    # counting the new data to store to display them in the log
    # provider - the service that offer data
    provider_token = service.provider.token
    service_provider = default_provider.get_service(
        str(service.provider.name.name))

    # check if the service has already been triggered
    # if date_triggered is None, then it's the first run
    if service.date_triggered is None:
        logger.debug("first time {}".format(service))
        to_update = True
        status = True
        # run run run
    else:
        # 1) get the data from the provider service
        # get a timestamp of the last triggered of the service
        kw = {'token': provider_token,
              'trigger_id': service.id,
              'date_triggered': service.date_triggered}
        getattr(service_provider, '__init__')(provider_token)
        data = getattr(service_provider, 'read_data')(**kw)
        # counting the new data to store to display them in the log
        count_new_data = len(data) if data else 0
        if count_new_data > 0:
            to_update = True
            status = True

    log_update(service, to_update, status, count_new_data)


def publishing(service):
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
        :param service: service object where we will publish
        :type service: object
    """
    # flag to know if we have to update
    to_update = False
    # flag to get the status of a service
    status = False
    # provider - the service that offer data
    # check if the service has already been triggered
    # if date_triggered is None, then it's the first run
    if service.date_triggered is None:
        logger.debug("first run {}".format(service))
        to_update = True
        status = True
    # run run run
    service_provider = default_provider.get_service(str(service.provider.name.name))
    
    # 1) get the data from the provider service
    kw = {'trigger_id': service.id}
    data = getattr(service_provider, 'process_data')(**kw)
    count_new_data = len(data) if data else 0
    if count_new_data > 0:
    
        # consumer - the service which uses the data
        service_consumer = default_provider.get_service(
                    str(service.consumer.name.name))
    
        getattr(service_consumer, '__init__')(service.consumer.token)
        consumer = getattr(service_consumer, 'save_data')
    
        # 2) for each one
        for d in data:
            # the consumer will save the data and return if success or not
            status = consumer(service.id, **d)
    
            to_update = True
        # let's log
    log_update(service, to_update, status, count_new_data)
    # let's update
    if to_update and status:
        update_trigger(service)
    

def recycle():
    """
        the purpose of this tasks is to recycle the data from the cache
        with version=2 in the main cache
    """
    all_packages = MyService.all_packages()
    for package in all_packages:
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
