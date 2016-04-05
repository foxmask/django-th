# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow

# django
from django.conf import settings
from django.core.cache import caches
from django.utils.log import getLogger
from django.db import connection

# django-rq
from django_rq import job

# trigger happy
from django_th.services import default_provider
from django_th.models import TriggerService
from django_th.my_services import MyService
from django_th.publishing_limit import PublishingLimit

# create logger
logger = getLogger('django_th.trigger_happy')


default_provider.load_services()


def log_update(service, to_update, status, count, action="to extract"):
    """
        lets log everything at the end
        :param service: service object
        :param to_update: boolean to check if we have to update
        :param status: is everything worked fine ?
        :param count: number of data to update
        :param action: "to publish" / "to extract"
        :type service: service object
        :type to_update: boolean
        :type status: boolean
        :type count: integer
        :type action: string
    """
    if to_update:
        if status:
            logger.info("{} - {} new data {}".format(service, count, action))
        else:
            logger.info("{} AN ERROR OCCURS ".format(service))
    else:
        logger.info("{} nothing new {}".format(service, action))


def update_trigger(trigger_id):
    """
        update the date when occurs the trigger
        :param trigger_id: id of the trigger
        :type trigger_id: int
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format(
        'YYYY-MM-DD HH:mm:ss')
    TriggerService.objects.filter(id=trigger_id).update(date_triggered=now)


def get_published(published='', which_date=''):
    """
       get the published date from the provider
       or set a default date (today in fact) if this service runs
       for the first time
       :param published: service object to update
       :param which_date: service object to update
       :type published: string data
       :type which_date: string date
    """
    if published is not None:
        # get the published date of the provider
        published = arrow.get(published).to(settings.TIME_ZONE)
        # store the date for the next loop
        #  if published became 'None'
        which_date = published
    # ... otherwise set it to 00:00:00 of the current date
    if which_date == '':
        # current date
        which_date = arrow.utcnow().replace(
            hour=0, minute=0, second=0).to(
            settings.TIME_ZONE)
        published = which_date
    if published is None and which_date != '':
        published = which_date
    return published, which_date


@job('default')
def reading(service):
    """
       get the data from the service and put theme in cache
       :param service: service object to read
    """
    # to avoid this #SSL SYSCALL error: EOF detected" with Postgresql
    # http://stackoverflow.com/questions/17523912/django-python-rq-databaseerror-ssl-error-decryption-failed-or-bad-record-mac
    # first close the connection
    connection.close()
    data = list()
    # flag to know if we have to update
    to_update = False
    # flag to get the status of a service
    status = False
    # counting the new data to store to display them in the log
    # provider - the service that offer data
    consumer_name = service.consumer.name.name
    consumer_token = service.consumer.token
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
        kw = {'token': consumer_token,
              'trigger_id': service.id,
              'date_triggered': service.date_triggered,
              'consumer': consumer_name,
              'model_name': consumer_name.split('Service')[1],
              }

        getattr(service_provider, '__init__')(service.provider.token or None)
        data = getattr(service_provider, 'read_data')(**kw)

        if len(data) > 0:
            to_update = True
            status = True
    cache = caches[str(service.provider.name)]
    cache.set('TRIGGERSERVICE_' + str(service.id), str(service))
    log_update(service, to_update, status, len(data))


@job('default')
def read_data():
    """
        The purpose of this tasks is to put data in cache
        because of the read_data function of each
        service
    """
    # to avoid this #SSL SYSCALL error: EOF detected" with Postgresql
    # http://stackoverflow.com/questions/17523912/django-python-rq-databaseerror-ssl-error-decryption-failed-or-bad-record-mac
    # first close the connection
    connection.close()
    trigger = TriggerService.objects.filter(status=True,
                                            user__is_active=True
                                            ).select_related(
        'consumer__name', 'provider__name')

    for service in trigger:
        reading.delay(service)


@job('high')
def publishing(service, trigger_id, token, payload, trigger):
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
        :param service: the service consumer
        :param trigger_id: id of the trigger
        :param token: token of the consumer
        :param payload: data coming from the cache
        :param trigger information coming from cache
        :type service: string
        :type trigger_id: integer
        :type token: string
        :type payload: list
        :type trigger: string
    """
    # to avoid this #SSL SYSCALL error: EOF detected" with Postgresql
    # http://stackoverflow.com/questions/17523912/django-python-rq-databaseerror-ssl-error-decryption-failed-or-bad-record-mac
    # first close the connection
    connection.close()
    status = False
    service_consumer = default_provider.get_service(service)
    # call the service consumer, pass the token
    getattr(service_consumer, '__init__')(token)
    consumer = getattr(service_consumer, 'save_data')

    for data in payload:
        # save the data !
        status = consumer(trigger_id, **data)

    # let's log
    log_update(trigger, True, status, len(payload), "published")
    # let's update
    if status:
        update_trigger(trigger_id)


@job('high')
def publish_data():
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
    """
    # to avoid this #SSL SYSCALL error: EOF detected" with Postgresql
    # http://stackoverflow.com/questions/17523912/django-python-rq-databaseerror-ssl-error-decryption-failed-or-bad-record-mac
    # first close the connection
    connection.close()
    # get all the services
    all_packages = MyService.all_packages()
    for package in all_packages:
        # get the cache of each service
        cache = caches[package]
        for service_cached in cache.iter_keys('Service*'):
            # do not handle string like "ServiceFoobar_TOKEN_xx"
            if "_TOKEN_" in service_cached:
                continue
            # eg split "ServiceRss_3"
            service, trigger_id = service_cached.split('_')
            cache_data = cache.get(service_cached) or list()
            data = PublishingLimit.get_data(service,
                                            cache_data,
                                            trigger_id)

            # only trigger a task if data are in the cache
            trigger = cache.get("TRIGGERSERVICE_" + trigger_id)
            if len(data) > 0:
                token = cache.get(service + "_TOKEN_" + trigger_id)
                publishing.delay(service, trigger_id, token, data, trigger)
            else:
                # let's log
                log_update(trigger, False, False, len(data), "to publish")


@job('low')
def get_outside_cache():
    """
        the purpose of this tasks is to recycle the data from the cache
        with version=2 in the main cache
    """
    all_packages = MyService.all_packages()
    for package in all_packages:
        cache = caches[package]
        # http://niwinz.github.io/django-redis/latest/#_scan_delete_keys_in_bulk
        for service in cache.iter_keys('Service*'):
            try:
                # get the value from the cache version=2
                service_value = cache.get(service, version=2)
                # put it in the version=1
                cache.set(service, service_value)
                # remove version=2
                cache.delete_pattern(service, version=2)
            except ValueError:
                pass
