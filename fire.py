#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
import time
import arrow

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_th.settings")
import django
django.setup()
from django.conf import settings
from django_th.services import default_provider
from django_th.models import TriggerService
from django.utils.log import getLogger

# create logger
logger = getLogger('django_th.trigger_happy')


def go():
    """
        run the main process
    """
    trigger = TriggerService.objects.filter(status=True)
    if trigger:
        for service in trigger:
            # flag to know if we have to update
            to_update = False
            # flag to get the status of a service
            status = False
            # counting the new data to store to display them in the log
            count_new_data = 0
            # provider - the service that offer datas
            service_name = str(service.provider.name.name)
            service_provider = default_provider.get_service(service_name)

            # consumer - the service which uses the data
            service_name = str(service.consumer.name.name)
            service_consumer = default_provider.get_service(service_name)

            # check if the service has already been triggered
            if service.date_triggered is None:
                logger.debug("first run for %s => %s " % (str(
                    service.provider.name), str(service.consumer.name.name)))
                to_update = True
            # run run run
            else:
                # 1) get the datas from the provider service
                # get a timestamp of the last triggered of the service
                datas = getattr(service_provider, 'process_data')(
                    service.provider.token, service.id, service.date_triggered)
                #consumer = getattr(service_consumer, 'save_data')

                published = ''
                which_date = ''

                # flag to know if we can push data to the consumer
                proceed = False

                # 2) for each one
                for data in datas:
                    # if in a pool of data once of them does not have
                    # a date, will take the previous date for this one
                    # if it's the first one, set it to 00:00:00

                    # let's try to determine the date contained in the data...
                    published = to_datetime(data)
                    if published is not None:
                        # get the published date of the provider
                        published = arrow.get(
                            str(published), 'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)
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
                    date_triggered = arrow.get(
                        str(service.date_triggered), 'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

                    # if the published date if greater or equal to the last
                    # triggered event ... :
                    if date_triggered is not None and published is not None and published.date() >= date_triggered.date():
                        # if date are the same ...
                        if published.date() == date_triggered.date():
                            # ... compare time and proceed if needed
                            if published.time() >= date_triggered.time():
                                proceed = True
                        # not same date so proceed !
                        else:
                            proceed = True

                        if proceed:
                            if 'title' in data:
                                logger.info("date {} >= date triggered {} title {}".format(
                                    published, date_triggered, data['title']))
                            else:
                                logger.info(
                                    "date {} >= date triggered {} ".format(published, date_triggered))

                            #status = consumer(
                            #    service.consumer.token, service.id, **data)

                            to_update = True
                            count_new_data += 1
                    # otherwise do nothing
                    else:
                        if 'title' in data:
                            logger.debug(
                                "data outdated skiped : [{}] {}".format(published, data['title']))
                        else:
                            logger.debug(
                                "data outdated skiped : [{}] ".format(published))

            # update the date of the trigger at the end of the loop
            sentance = "user: {} - provider: {} - consumer: {} - {}"
            if to_update:
                if status:
                    logger.info((sentance + " new data").format(
                        service.user,
                        service.provider.name.name,
                        service.consumer.name.name,
                        service.description,
                        count_new_data))
                    update_trigger(service)
                else:
                    logger.info((sentance + " AN ERROR OCCURS ").format(
                        service.user,
                        service.provider.name.name,
                        service.consumer.name.name,
                        service.description))
            else:
                logger.info((sentance + " nothing new").format(
                    service.user,
                    service.provider.name.name,
                    service.consumer.name.name,
                    service.description))
    else:
        print("No trigger set by any user")


def update_trigger(service):
    """
        update the date when occurs the trigger
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ss')
    TriggerService.objects.filter(id=service.id).update(date_triggered=now)


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
    elif 'my_date' in data:
        my_date_time = arrow.get(str(data['my_date']), 'YYYY-MM-DD HH:mm:ss')

    return my_date_time


def main():
    default_provider.load_services()
    # let's go
    go()

if __name__ == "__main__":

    main()
