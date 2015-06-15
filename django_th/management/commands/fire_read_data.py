#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from django_th.services import default_provider
from django_th.models import TriggerService
from django.utils.log import getLogger
# create logger
logger = getLogger('django_th.trigger_happy')


class Command(BaseCommand):
    help = 'Trigger all the services to put them in cache'

    def handle(self, *args, **options):
        """
            run the main process
        """
        default_provider.load_services()
        trigger = TriggerService.objects.filter(status=True).select_related(
            'consumer__name', 'provider__name')

        for service in trigger:
            self.put_in_cache.delay(service)

    def put_in_cache(self, service):
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
