# coding: utf-8
from django.conf import settings


def _get_service_long(package, topic):
    service_long = ''
    service_name = package.split('_')[1]
    service_long = ''.join((package, ".my_", service_name, ".Service",
                            service_name.title()))
    if service_long in settings.TH_SERVICES:
        if topic == 'service_long':
            return service_long
        elif topic == 'module_name':
            return "".join("my_", service_name)
        elif topic == 'service_name':
            return "".join("Service", service_name.title())
    return service_long


class MyService(object):
    """
        class to get the name of the package, module, class
        from the TH_SERVICES settings
    """

    @staticmethod
    def service_long(package):

        service_long = ''
        if package.startswith('th_'):
            service_long = _get_service_long(package, 'service_long')
        return service_long

    @staticmethod
    def module_name(package):
        module_name = ''
        if package.startswith('th_'):
            module_name = _get_service_long(package, 'module_name')
        return module_name

    @staticmethod
    def service_name(package):

        service_name = ''
        if package.startswith('th_'):
            service_name = _get_service_long(package, 'service_long')
        return service_name

    @staticmethod
    def all_packages():
        my_services = []
        for services in settings.TH_SERVICES:
            package = services.split('.')[0]
            my_services.append(package)
        return my_services
