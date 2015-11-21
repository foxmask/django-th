# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import datetime
import time
import arrow

from celery import shared_task, chain

from django.conf import settings
from django.core.cache import caches
from django_th.services import default_provider
from django_th.models import TriggerService
from django_th.my_services import MyService

from django.utils.log import getLogger
# create logger
logger = getLogger('django_th.trigger_happy')


default_provider.load_services()


def publish_log_outdated(published, data):
    """
        lets log things about outdated data
        or data from the future... (a date from the future)
    """
    if 'title' in data:
        sentence = "data outdated skipped : [{}] {}"
        logger.debug(sentence.format(published,
                                     data['title']))
    else:
        sentence = "data outdated skipped : [{}] "
        logger.debug(sentence.format(published))


def publish_log_data(published, date_triggered, data):
    """
        lets log everything linked to the data
    """
    if 'title' in data:
        sentence = "date {} >= triggered {} title {}"
        logger.info(sentence.format(published,
                                    date_triggered,
                                    data['title']))
    else:
        sentence = "date {} >= date triggered {}"
        logger.info(sentence.format(published,
                                    date_triggered))


def log_update(service, to_update, status, count):
    """
        lets log everything at the end
    """
    if to_update:
        if status:
            logger.info("{} - {} new data".format(service, count))
        else:
            logger.info("{} AN ERROR OCCURS ".format(service))
    else:
        logger.info("{} nothing new ".format(service))


def update_trigger(service):
    """
        update the date when occurs the trigger
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format(
        'YYYY-MM-DD HH:mm:ss')
    TriggerService.objects.filter(id=service.id).update(date_triggered=now)


def to_datetime(data):
    """
        convert Datetime 9-tuple to the date and time format
        feedparser provides this 9-tuple
    """
    my_date_time = None

    if 'published_parsed' in data:
        my_date_time = datetime.datetime.utcfromtimestamp(
            time.mktime(data.published_parsed))
    elif 'updated_parsed' in data:
        my_date_time = datetime.datetime.utcfromtimestamp(
            time.mktime(data.updated_parsed))
    elif 'my_date' in data:
        my_date_time = arrow.get(data['my_date'])

    return my_date_time


def get_published(published='', which_date=''):
    """
       get the published date from the provider
       or set a default date (today in fact) if this service runs
       for the first time
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


@shared_task
def reading(service):
    # flag to know if we have to update
    to_update = False
    # flag to get the status of a service
    status = False
    # counting the new data to store to display them in the log
    # provider - the service that offer data
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
        datas = getattr(service_provider, '__init__')(service.provider.token)
        datas = getattr(service_provider, 'read_data')(
            service.provider.token,
            service.id,
            service.date_triggered)
        if len(datas) > 0:
            to_update = True
            status = True

        log_update(service, to_update, status, len(datas))


@shared_task
def read_data():
    """
        The purpose of this tasks is to put data in cache
        because of the read_data function of each
        service
    """
    trigger = TriggerService.objects.filter(status=True).select_related(
        'consumer__name', 'provider__name')

    for service in trigger:
        reading.delay(service)


@shared_task
def publishing(service, now):
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
    """
    # flag to know if we have to update
    to_update = False
    # flag to get the status of a service
    status = False
    # counting the new data to store to display them in the log
    count_new_data = 0
    # provider - the service that offer data
    service_provider = default_provider.get_service(
        str(service.provider.name.name))

    # consumer - the service which uses the data
    service_consumer = default_provider.get_service(
        str(service.consumer.name.name))

    # check if the service has already been triggered
    # if date_triggered is None, then it's the first run
    if service.date_triggered is None:
        logger.debug("first run {}".format(service))
        to_update = True
        status = True
    # run run run
    else:
        # 1) get the data from the provider service
        # get a timestamp of the last triggered of the service
        datas = getattr(service_provider, 'process_data')(service.id)
        if datas is None or len(datas) == 0:
            continue
        consumer = getattr(service_consumer, '__init__')(
            service.consumer.token)
        consumer = getattr(service_consumer, 'save_data')

        published = ''
        which_date = ''
        # 2) for each one
        for data in datas:
            # if in a pool of data once of them does not have
            # a date, will take the previous date for this one
            # if it's the first one, set it to 00:00:00

            # let's try to determine the date contained in
            # the data...
            published = to_datetime(data)
            published, which_date = get_published(published,
                                                  which_date)
            # 3) check if the previous trigger is older than the
            # date of the data we retrieved
            # if yes , process the consumer

            # add the TIME_ZONE settings
            # to localize the current date
            date_triggered = arrow.get(
                str(service.date_triggered),
                'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

            # if the published date is greater or equal to the last
            # triggered event ... :
            if date_triggered is not None and \
               published is not None and \
               now >= published and \
               published >= date_triggered:

                publish_log_data(published, date_triggered, data)

                status = consumer(
                    service.consumer.token, service.id, **data)

                to_update = True
                count_new_data += 1
            # otherwise do nothing
            else:
                publish_log_outdated(published, data)

    log_update(service, to_update, status, count_new_data)
    if to_update and status:
        update_trigger(service)


@shared_task
def publish_data(result=''):
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
    """
    now = arrow.utcnow().to(settings.TIME_ZONE)
    trigger = TriggerService.objects.filter(status=True).select_related(
        'consumer__name', 'provider__name')

    for service in trigger:
        publishing.delay(service, now)


@shared_task
def get_outside_cache(result=''):
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


@shared_task
def go():
    chain(read_data.s(), publish_data.s(), get_outside_cache.s())()
