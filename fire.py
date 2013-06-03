#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
import time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_th.settings")
from django_th.services import default_provider
from django_th.models import TriggerService
from django.utils.log import getLogger

# create logger
logger = getLogger('django_th.trigger_happy')


# todo
# 1) abstract the ".published" properties or add it to each service


def go():
    """
        run the main process
    """
    to_update = False
    trigger = TriggerService.objects.all()
    if trigger:
        for service in trigger:
            logger.info(
                "PROVIDER %s CONSUMMER %s ", service.provider.name, service.consummer.name)

            # provider - the service that offer datas
            service_name = str(service.provider.name)
            service_provider = default_provider.get_service(service_name)

            # consummer - the service which uses the datas
            service_name = str(service.consummer.name)
            service_consummer = default_provider.get_service(service_name)

            # check if the service has already been triggered
            if service.date_triggered is None:
                logger.debug("first run for %s => %s " % (str(
                    service.provider.name), str(service.consummer.name)))
                to_update = True
            # run run run
            else:
                extra = {}
                # 1) get the datas from the provider service
                datas = getattr(service_provider, 'process_data')(service.id)
                consummer = getattr(service_consummer, 'save_data')

                # 2) for each one
                for data in datas:
                    title = data.title
                    if 'content' in data:
                        content = data.content[0].value
                    else:
                        content = data.description
                    # 3) check if the previous trigger is older than the
                    # date of the data we retreived
                    # if yes , process the consummer
                    if service.date_triggered is not None and \
                            to_datetime(data.published_parsed) >= service.date_triggered:
                        logger.debug(
                            "date %s title %s", data.published, data.title)

                        extra = {'link': data.link}
                        consummer(
                            service.consummer.token, title, content, service.id, extra)
                        to_update = True
                    # otherwise do nothing
                    else:
                        logger.debug(
                            "data outdated skiped : [%s] %s", data.published, data.title)
            # update the date of the trigger
            if to_update:
                update_trigger(service)

    else:
        print "No trigger set by any user"


def update_trigger(service):
    """
        update the date when occurs the trigger
    """
    trigger = TriggerService.objects.get(id=service.id)
    if trigger:
        trigger.date_triggered = datetime.datetime.now()
        trigger.save()


def to_datetime(my_date_string):
    """
        convert Datetime 9-tuple to the date and time format
        feedparser provides this 9-tuple
    """
    return datetime.datetime.fromtimestamp(time.mktime(my_date_string))


def main():
    default_provider.load_services()
    # let's go
    go()

if __name__ == "__main__":

    main()
