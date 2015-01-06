#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import time
import arrow

from django.core.management.base import BaseCommand
from django.conf import settings
from django_th.services import default_provider
from django_th.models import TriggerService
from django.utils.log import getLogger
# create logger
logger = getLogger('django_th.trigger_happy')


class Command(BaseCommand):

    help = 'Trigger all the services'

    def update_trigger(self, service):
        """
            update the date when occurs the trigger
        """
        now = arrow.utcnow().to(settings.TIME_ZONE).format(
            'YYYY-MM-DD HH:mm:ss')
        TriggerService.objects.filter(id=service.id).update(date_triggered=now)

    def to_datetime(self, data):
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
            my_date_time = arrow.get(str(data['my_date']),
                                     'YYYY-MM-DD HH:mm:ss')

        return my_date_time

    def handle(self, *args, **options):
        """
            run the main process
        """
        default_provider.load_services()
        trigger = TriggerService.objects.filter(status=True).select_related('consumer__name', 'provider__name')
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
                # if date_triggered is None, then it's the first run
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
                    datas = getattr(service_provider, 'process_data')(
                        service.provider.token, service.id,
                        service.date_triggered)
                    consumer = getattr(service_consumer, 'save_data')

                    published = ''
                    which_date = ''

                    # 2) for each one
                    for data in datas:
                        # if in a pool of data once of them does not have
                        # a date, will take the previous date for this one
                        # if it's the first one, set it to 00:00:00

                        # let's try to determine the date contained in
                        # the data...
                        published = self.to_datetime(data)

                        if published is not None:
                            # get the published date of the provider
                            published = arrow.get(str(published), 'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)
                            # store the date for the next loop
                            # if published became 'None'
                            which_date = published
                        #... otherwise set it to 00:00:00 of the current date
                        if which_date == '':
                            # current date
                            which_date = arrow.utcnow().replace(hour=0, minute=0, second=0).to(settings.TIME_ZONE)
                            published = which_date
                        if published is None and which_date != '':
                            published = which_date
                        # 3) check if the previous trigger is older than the
                        # date of the data we retrieved
                        # if yes , process the consumer

                        # add the TIME_ZONE settings
                        # to localize the current date
                        date_triggered = arrow.get(str(service.date_triggered), 'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

                        # if the published date if greater or equal to the last
                        # triggered event ... :
                        if date_triggered is not None and \
                           published is not None and \
                           published >= date_triggered:

                            if 'title' in data:
                                logger.info("date {} >= date triggered {} title {}".format(published, date_triggered, data['title']))
                            else:
                                logger.info("date {} >= date triggered {} ".format(published, date_triggered))

                            status = consumer(
                                service.consumer.token, service.id, **data)

                            to_update = True
                            count_new_data += 1
                        # otherwise do nothing
                        else:
                            if 'title' in data:
                                logger.debug("data outdated skipped : [{}] {}".format(published, data['title']))
                            else:
                                logger.debug("data outdated skipped : [{}] ".format(published))

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
                        self.update_trigger(service)
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
        else:
            self.stdout.write("No trigger set by any user")
