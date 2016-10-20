# coding: utf-8
from django.conf import settings
from django.core.cache import caches
from django_th.my_services import MyService


class PublishingLimit(object):

    """
        this class permits to reduce the quantity of data to be pulibshed
        get the limit from settings.DJANGO_TH['publishing_limit']
        if the limit does not exist, it returns everything
    """
    @staticmethod
    def get_data(service, cache_data, trigger_id):
        """
            get the data from the cache
            :param service: the service name
            :param cache_data: the data from the cache
            :type trigger_id: integer
            :return: Return the data from the cache
            :rtype: object
        """

        # rebuild the string
        # th_<service>.my_<service>.Service<Service>
        if service.startswith('th_'):
            service_long = MyService.full_name(service)
            # ... and check it
            if service_long in settings.TH_SERVICES:

                cache = caches[service]

                limit = settings.DJANGO_TH.get('publishing_limit', 0)

                # publishing of all the data
                if limit == 0:
                    return cache_data
                # or just a set of them
                if cache_data is not None and len(cache_data) > limit:
                    for data in cache_data[limit:]:
                        service_str = ''.join((service, '_',
                                               str(trigger_id)))
                        # put that data in a version 2 of the cache
                        cache.set(service_str, data, version=2)
                        # delete data from cache version=1
                        # https://niwinz.github.io/django-redis/latest/#_scan_delete_keys_in_bulk
                        cache.delete_pattern(service_str)
                    # put in cache unpublished data
                    cache_data = cache_data[:limit]

        return cache_data
