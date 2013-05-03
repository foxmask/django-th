#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_th.settings")
from django_th.services import default_provider
from django_th.models import TriggerService


def go():

    trigger = TriggerService.objects.all()
    for service in trigger:
        print "from %s to %s " % (service.provider, service.consummer)
        service_name = 'Service' + str(service.provider).capitalize()
        service_provider = default_provider.get_service(service_name)
        service_name = 'Service' + str(service.consummer).capitalize()
        service_consummer = default_provider.get_service(service_name)

        datas = getattr(service_provider, 'process_data')(service.id)
        consummer = getattr(service_consummer, 'process_data')
        for data in datas:
            print data
            consummer(service.id, data)


def main():
    default_provider.load_services()
    go()

if __name__ == "__main__":

    main()
    # from django.core.management import execute_from_command_line
