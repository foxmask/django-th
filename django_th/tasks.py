# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import datetime
import time
import arrow

from celery import shared_task

from django.conf import settings
from django_th.services import default_provider
from django_th.models import TriggerService

from django.utils.log import getLogger
# create logger
logger = getLogger('django_th.trigger_happy')


default_provider.load_services()


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
        my_date_time = arrow.get(str(data['my_date']),
                                 'YYYY-MM-DD HH:mm:ss')

    return my_date_time


@shared_task
def put_in_cache(service):
    # flag to know if we have to update
    to_update = False
    # flag to get the status of a service
    status = False
    # counting the new data to store to display them in the log
    # provider - the service that offer data
    service_name = str(service.provider.name.name)
    service_provider = default_provider.get_service(service_name)

    service_name = str(service.consumer.name.name)

    # check if the service has already been triggered
    # if date_triggered is None, then it's the first run
    if service.date_triggered is None:
        logger.debug("first run for %s => %s " % (
            str(service.provider.name), str(service.consumer.name.name)))
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

        # update the date of the trigger at the end of the loop
        sentence = "user: {} - provider: {} - {}"
        if to_update:
            if status:
                logger.info((sentence + " - {} data put in cache").format(
                    service.user,
                    service.provider.name.name,
                    service.description,
                    len(datas)))
            else:
                logger.info((sentence + " AN ERROR OCCURS ").format(
                    service.user,
                    service.provider.name.name,
                    service.description))
        else:
            logger.info((sentence + " nothing new").format(
                        service.user,
                        service.provider.name.name,
                        service.description))


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
        put_in_cache.delay(service)


@shared_task
def publish_data():
    """
        the purpose of this tasks is to get the data from the cache
        then publish them
    """
    now = arrow.utcnow().to(settings.TIME_ZONE)

    trigger = TriggerService.objects.filter(status=True).select_related(
        'consumer__name', 'provider__name')
    if trigger:
        for service in trigger:

            # flag to know if we have to update
            to_update = False
            # flag to get the status of a service
            status = False
            # counting the new data to store to display them in the log
            count_new_data = 0
            # provider - the service that offer data
            service_name = str(service.provider.name.name)
            service_provider = default_provider.get_service(service_name)

            # consumer - the service which uses the data
            service_name = str(service.consumer.name.name)
            service_consumer = default_provider.get_service(service_name)

            # check if the service has already been triggered
            # if date_triggered is None, then it's the first run
            if service.date_triggered is None:
                logger.debug("first run for %s => %s " % (str(
                    service.provider.name),
                    str(service.consumer.name.name)))
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
                    #  if in a pool of data once of them does not have
                    #  a date, will take the previous date for this one
                    #  if it's the first one, set it to 00:00:00

                    # let's try to determine the date contained in
                    # the data...
                    published = to_datetime(data)

                    if published is not None:
                        # get the published date of the provider
                        published = arrow.get(
                            str(published),
                            'YYYY-MM-DD HH:mm:ss').to(
                            settings.TIME_ZONE)
                        # store the date for the next loop
                        #  if published became 'None'
                        which_date = published
                    # ... otherwise set it to 00:00:00 of the current date
                    if which_date == '':
                        # current date
                        which_date = arrow.utcnow().replace(
                            hour=0, minute=0, second=0).to(
                            settings.TIME_ZONE)
                        published = which_date
                    if published is None and which_date != '':
                        published = which_date
                    # 3) check if the previous trigger is older than the
                    #  date of the data we retrieved
                    #  if yes , process the consumer

                    # add the TIME_ZONE settings
                    # to localize the current date
                    date_triggered = arrow.get(
                        str(service.date_triggered),
                        'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

                    # if the published date if greater or equal to the last
                    # triggered event ... :
                    if date_triggered is not None and \
                       published is not None and \
                       now >= published and \
                       published >= date_triggered:

                        if 'title' in data:
                            sentence = "date {} >= triggered {} title {}"
                            logger.info(sentence.format(published,
                                                        date_triggered,
                                                        data['title']))
                        else:
                            sentence = "date {} >= date triggered {}"
                            logger.info(sentence.format(published,
                                                        date_triggered))

                        status = consumer(
                            service.consumer.token, service.id, **data)

                        to_update = True
                        count_new_data += 1
                    # otherwise do nothing
                    else:
                        if 'title' in data:
                            sentence = "data outdated skipped : [{}] {}"
                            logger.debug(sentence.format(published,
                                                         data['title']))
                        else:
                            sentence = "data outdated skipped : [{}] "
                            logger.debug(sentence.format(published))

            # update the date of the trigger at the end of the loop
            sentence = "user: {} - provider: {} - consumer: {} - {}"
            if to_update:
                if status:
                    logger.info((sentence + " - {} new data").format(
                        service.user,
                        service.provider.name.name,
                        service.consumer.name.name,
                        service.description,
                        count_new_data))
                    update_trigger(service)
                else:
                    logger.info((sentence + " AN ERROR OCCURS ").format(
                        service.user,
                        service.provider.name.name,
                        service.consumer.name.name,
                        service.description))
            else:
                logger.info((sentence + " nothing new").format(
                    service.user,
                    service.provider.name.name,
                    service.consumer.name.name,
                    service.description))
