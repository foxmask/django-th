# coding: utf-8
from django.conf import settings


class MyService(object):

    """
        build the name of the package, module, class
        on that model:
        th_<service>.my_<service>.Service<Service>
    """
    @staticmethod
    def full_name(service):
        service_name = service.split('Service')[1].lower()
        return ''.join(("th_" + service_name,
                        ".my_",
                        service_name,
                        ".",
                        service))

    @staticmethod
    def module_name(package):
        return "".join(("my_", package.split('_')[1]))

    @staticmethod
    def service_name(package):
        return "".join(("Service", package.split('_')[1].title()))

    @staticmethod
    def all_packages():
        my_services = list()
        for services in settings.TH_SERVICES:
            package = services.split('.')[2]
            my_services.append(package)
        return my_services
