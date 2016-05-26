# coding: utf-8
from django.conf import settings
from collections import OrderedDict


class ServiceProvider(OrderedDict):

    def load_services(self, services=settings.TH_SERVICES):
        """
            get the service from the settings
        """
        kwargs = {}
        for class_path in services:
            module_name, class_name = class_path.rsplit('.', 1)
            klass = import_from_path(class_path)
            service = klass(None, **kwargs)
            self.register(class_name, service)

    def register(self, class_name, service):
        self[class_name] = service

    def get_service(self, class_name):
        """
            get the service (class instance) from its name
        """
        return self[class_name]


def import_from_path(path):
    """
        Import a class dynamically, given it's dotted path.
        :param path: the path of the module
        :type path: string
        :return: Return the value of the named attribute of object.
        :rtype: object
    """
    module_name, class_name = path.rsplit('.', 1)
    try:
        return getattr(__import__(module_name,
                                  fromlist=[class_name]), class_name)
    except AttributeError:
        raise ImportError('Unable to import %s' % path)

service_provider = ServiceProvider()
