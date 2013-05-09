#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_th.settings")
from django_th.services import default_provider
from django_th.models import TriggerService


# todo
# 1) manage log to trace whats happened
# 2) abstract the ".published" properties or add it to each service

def go():
    """
        run the main process
    """
    trigger = TriggerService.objects.all()
    for service in trigger:
        print "from %s to %s " % (service.provider, service.consummer)

        # provider - the service that offer datas
        service_name = 'Service' + str(service.provider).capitalize()
        service_provider = default_provider.get_service(service_name)

        # consummer - the service which uses the datas
        service_name = 'Service' + str(service.consummer).capitalize()
        service_consummer = default_provider.get_service(service_name)

        # 1) get the datas from the provider service
        datas = getattr(service_provider, 'process_data')(service.id)
        consummer = getattr(service_consummer, 'process_data')

        # 2) for each one
        for data in datas:
            # 3) check if the previous trigger is older than the
            # date of the data we retreived
            # if yes , process the consummer
            if service.date_triggered is None or\
                    to_datetime(data.published) >= service.date_triggered:
                print data.published, data.title
                consummer(service.id, data)
            # otherwise do nothing
            else:
                # todo log vs print
                print "nothing to update nor trigger"
            # update the date of the trigger
            update_trigger(service)


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
    # load the services
    default_provider.load_services()
    # let's go
    go()

if __name__ == "__main__":

    main()
