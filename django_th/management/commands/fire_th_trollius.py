#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
import time
import arrow
import trollius as asyncio
from trollius import From

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django_th.services import default_provider
from django_th.models import TriggerService
from django.utils.log import getLogger

# create logger
logger = getLogger('django_th.trigger_happy')

q = asyncio.Queue(maxsize=0)
q2 = asyncio.Queue(maxsize=0)


def to_datetime(data):
    """
        convert Datetime 9-tuple to the date and time format
        feedparser provides this 9-tuple
    """
    my_date_time = None

    if 'published_parsed' in data:
        my_date_time = datetime.datetime.fromtimestamp(
            time.mktime(data.published_parsed))
    elif 'updated_parsed' in data:
        my_date_time = datetime.datetime.fromtimestamp(
            time.mktime(data.updated_parsed))

    return my_date_time


class Command(BaseCommand):

    @asyncio.coroutine
    def update_trigger(self, service):
        """
            update the date when occurs the trigger
        """
        my_count = yield From(q2.get())
        if my_count > 0:

            logger.info("user: {} - provider: {} - consumer: {} - {} = {} new data".format(
                service.user, service.provider.name.name, service.consumer.name.name, service.description, my_count))

            now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ss')
            TriggerService.objects.filter(id=service.id).update(date_triggered=now)
        else:
            logger.info("user: {} - provider: {} - consumer: {} - {} nothing new".format(
                service.user, service.provider.name.name, service.consumer.name.name, service.description))
        asyncio.get_event_loop().stop()

    @asyncio.coroutine
    def my_dummy_provider(self):
        """
            just a dummy provider when its the first time
            the trigger is handling
        """
        yield From(q2.put(1))

    @asyncio.coroutine
    def my_provider(self, service_provider, token, service_id, date_triggered):
        """
            service_provider : the name of the class to trigger the service
            token : is the token of the service provider from the database
            service_id : is the service id from the database
            date_triggered : date_triggered is the data from the database
        """
        datas = getattr(service_provider, 'process_data')(
            token, service_id, date_triggered)

        for data in datas:
            yield From(q.put(data))

    @asyncio.coroutine
    def my_consumer(self, service_consumer, token, service_id, date_triggered):
        """
            service_consumer : the name of the consumer 'service' class
            token : is the token of the service consumer
            service_id : is the service id from the database
            date_triggered : date_triggered is the data from the database
        """
        count_new_data = 0
        while q.empty() is not True:
            data = yield From(q.get())

            consumer = getattr(service_consumer, 'save_data')

            published = ''
            which_date = ''

            # flag to know if we can push data to the consumer

            # 2) for each one
            # if in a pool of data once of them does not have
            # a date, will take the previous date for this one
            # if it's the first one, set it to 00:00:00
            # let's try to determine the date contained in the data...
            published = to_datetime(data)
            if published is not None:
                # get the published date of the provider
                published = arrow.get(str(published), 'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)
                # store the date for the next loop
                # if published became 'None'
                which_date = published
            #... otherwise set it to 00:00:00 of the current date
            if which_date == '':
                # current date
                which_date = arrow.utcnow().replace(
                    hour=0, minute=0, second=0)
                published = which_date
            if published is None and which_date != '':
                published = which_date
            # 3) check if the previous trigger is older than the
            # date of the data we retreived
            # if yes , process the consumer

            # add the TIME_ZONE settings
            my_date_triggered = arrow.get(
                str(date_triggered), 'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

            # if the published date if greater or equal to the last
            # triggered event ... :
            if date_triggered is not None and \
               published is not None and \
               published >= date_triggered:

                if 'title' in data:
                    logger.info("date {} >= date triggered {} title {}".format(
                        published, date_triggered, data['title']))
                else:
                    logger.info(
                        "date {} >= date triggered {} ".format(published, my_date_triggered))

                consumer(token, service_id, **data)

                count_new_data += 1
            # otherwise do nothing
            else:
                if 'title' in data:
                    logger.debug(
                        "data outdated skipped : [{}] {}".format(published, data['title']))
                else:
                    logger.debug(
                        "data outdated skipped : [{}] ".format(published))

        # return the number of updates ( to be displayed in the log )
        yield From(q2.put(count_new_data))

    def handle(self, *args, **options):
        """
            run the main process
        """
        default_provider.load_services()
        trigger = TriggerService.objects.filter(status=True).select_related('consumer__name', 'provider__name')
        if trigger:
            for service in trigger:

                # provider - the service that offer data
                service_name = str(service.provider.name.name)
                service_provider = default_provider.get_service(service_name)

                # consumer - the service which uses the data
                service_name = str(service.consumer.name.name)
                service_consumer = default_provider.get_service(service_name)

                # First run
                if service.date_triggered is None:
                    logger.debug("first run for %s => %s " % (str(
                        service.provider.name), str(service.consumer.name.name)))

                    asyncio.get_event_loop().run_until_complete(self.my_dummy_provider())

                # another run
                else:
                    asyncio.get_event_loop().run_until_complete(
                        self.my_provider(service_provider, service.provider.token, service.id, service.date_triggered))
                    asyncio.get_event_loop().run_until_complete(
                        self.my_consumer(service_consumer, service.consumer.token, service.id, service.date_triggered))

                asyncio.get_event_loop().run_until_complete(self.update_trigger(service))
                asyncio.get_event_loop().run_forever()

        else:
            print("No trigger set by any user")
