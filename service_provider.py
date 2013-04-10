# -*- coding: utf-8 -*-
from ordereddict import OrderedDict
from django.conf import settings
from batbelt.objects import import_from_path


class ServiceProvider(OrderedDict):
    """
        get the service from the settings
    """
    def load_services(self, services=settings.TH_SERVICES):

        for class_path in services:
            module_name, class_name = class_path.rsplit('.', 1)
            klass = import_from_path(class_path)
            service = klass()
            self.register(class_name, service)

    def register(self, class_name, service):
        self[class_name] = service

    """
        get the service (class instance) from its name
    """
    def get_service(self, class_name):
        return self[class_name]

service_provider = ServiceProvider()
