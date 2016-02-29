# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow

# django
from django.conf import settings
from django.core.cache import caches
from django.utils.log import getLogger

# django-rq
from django_rq import job

# trigger happy
from django_th.services import default_provider
from django_th.models import TriggerService
from django_th.my_services import MyService

# create logger
logger = getLogger('django_th.trigger_happy')


default_provider.load_services()


def publish_log_outdated(published, data):
    """
        lets log things about outdated data
        or data from the future... (a date from the future)
        :param published: publishing date
        :param data: the data of the current trigger
        :type published: string date
        :type data: dict
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
        :param published: publishing date
        :param date_triggered: the last time a trigger has been proceeded
        :param data: the data of the current trigger
        :type published: string date
        :type date_triggered: string date
        :type data: dict
    """
    if 'title' in data:
        sentence = "date {} >= triggered {} title {}"
        logger.debug(sentence.format(published,
                                     date_triggered,
                                     data['title']))
    else:
        sentence = "date {} >= date triggered {}"
        logger.debug(sentence.format(published,
                                     date_triggered))


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
            logger.info("{} AN ERROR OCCURS ".format(service))
    else:
        logger.info("{} nothing new ".format(service))


def update_trigger(service):
    """
        update the date when occurs the trigger
        :param service: service object to update
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format(
        'YYYY-MM-DD HH:mm:ss')
    TriggerService.objects.filter(id=service.id).update(date_triggered=now)


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


@job
def reading(service):
    """
       get the data from the service and put theme in cache
       :param service: service object to read
    """
    datas = ()
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
        kw = {'token': service.provider.token,
              'trigger_id': service.id,
              'date_triggered': service.date_triggered}
        datas = getattr(service_provider, '__init__')(service.provider.token)
        datas = getattr(service_provider, 'read_data')(**kw)

        if len(datas) > 0:
            to_update = True
            status = True

    log_update(service, to_update, status, len(datas))


@job
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


@job('high')
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
        kw = {'trigger_id': service.id}
        datas = getattr(service_provider, 'process_data')(**kw)
        if datas is not None and len(datas) > 0:
            consumer = getattr(service_consumer, '__init__')(
                service.consumer.token)
            consumer = getattr(service_consumer, 'save_data')

            published = ''
            which_date = ''

            # 2) for each one
            for data in datas:

                if settings.DEBUG:
                    from django_th.tools import to_datetime
                    published = to_datetime(data)
                    published, which_date = get_published(published,
                                                          which_date)
                    date_triggered = arrow.get(
                        str(service.date_triggered),
                        'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)
                    publish_log_data(published, date_triggered, data)
                # the consummer will save the data and return if success or not
                status = consumer(service.consumer.token, service.id, **data)
            else:
                count_new_data = len(datas)
                to_update = True
    # let's log
    log_update(service, to_update, status, count_new_data)
    # let's update
    if to_update and status:
        update_trigger(service)


@job('high')
def publish_data():
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
    """
    trigger = TriggerService.objects.filter(status=True).select_related(
        'consumer__name', 'provider__name')

    for service in trigger:
        publishing.delay(service)


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
