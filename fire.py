#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime

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
    trigger = TriggerService.objects.all()
    if trigger:
        for service in trigger:
            logger.info(
                "from %s to %s ", service.provider.name, service.consummer.name)

            # provider - the service that offer datas
            service_name = service.provider.name
            service_provider = default_provider.get_service(service_name)

            # consummer - the service which uses the datas
            service_name = service.consummer.name
            service_consummer = default_provider.get_service(service_name)

            # 1) get the datas from the provider service
            datas = getattr(service_provider, 'process_data')(service.id)
            consummer = getattr(service_consummer, 'save_data')

            # 2) for each one
            for data in datas:
                title = data.title
                content = data.content[0].value
                logger.info("from the service %s", service.provider)
                # 3) check if the previous trigger is older than the
                # date of the data we retreived
                # if yes , process the consummer
                if service.date_triggered is None or to_datetime(data.published) >= service.date_triggered:
                    logger.debug(
                        "date %s title %s", data.published, data.title)
                    logger.info("to the service %s", service.consummer)
                    consummer(
                        service.consummer.token, title, content, service.id)
                # otherwise do nothing
                else:
                    logger.debug(
                        "DATA TOO OLD SKIPED : [%s] %s", data.published, data.title)
                # update the date of the trigger
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
        convert string to date eg
        "Sat, 04 May 2013 09:55:17 +0000" to "2013-05-04 09:55:17"
    """
    # drop the string tz from the string to avoid
    # an issue with %z in format eg :
    # strptime(my_date_string[:-6], "%a, %d %b %Y %H:%M:%S %z")
    # also the Setting HAS TO BE =>>> USE_TZ = False
    # or error occurs :
    # can't compare offset-naive and offset-aware datetimes
    return datetime.datetime.strptime(my_date_string[:-6], "%a, %d %b %Y %H:%M:%S")


def main():
    default_provider.load_services()
    # let's go
    go()

if __name__ == "__main__":

    main()
