# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow
# django
from django.utils.log import getLogger
from django.conf import settings

# trigger happy
from django_th.services import default_provider

logger = getLogger('django_th.trigger_happy')


class Read(object):
    """
        Extracting the data from any service
    """
    def provider(self, service_provider, **kwargs):
        """
            get the data of the provider service
            :param service_provider:
            :param kwargs:
            :return:
        """
        getattr(service_provider, '__init__')(kwargs.get('token'))
        return getattr(service_provider, 'read_data')(**kwargs)

    def reading(self, service):
        """
           get the data from the service and put theme in cache
           :param service: service object to read
           :type service: object
        """
        now = arrow.utcnow().to(settings.TIME_ZONE).format(
            'YYYY-MM-DD HH:mm:ssZZ')
        # flag to know if we have to update
        to_update = False

        # counting the new data to store to display them in the log
        # provider - the service that offer data
        provider_token = service.provider.token
        default_provider.load_services()
        service_provider = default_provider.get_service(
            str(service.provider.name.name))
        # check if the service has already been triggered
        # if date_triggered is None, then it's the first run
        # so it will be set to "now"
        date_triggered = service.date_triggered if service.date_triggered \
            else now
        # 1) get the data from the provider service
        # get a timestamp of the last triggered of the service
        kwargs = {'token': provider_token,
                  'trigger_id': service.id,
                  'date_triggered': date_triggered}
        data = self.provider(service_provider, **kwargs)
        # counting the new data to store to display them in the log
        count_new_data = len(data) if data else 0
        if count_new_data > 0:
            to_update = True

        if to_update:
            logger.info("{} - {} new data".format(service, count_new_data))
