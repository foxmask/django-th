# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

# django
from django.utils.log import getLogger

# trigger happy
from django_th.services import default_provider

logger = getLogger('django_th.trigger_happy')

default_provider.load_services()


def reading(service):
    """
       get the data from the service and put theme in cache
       :param service: service object to read
       :type service: object
    """
    # flag to know if we have to update
    to_update = False
    count_new_data = 0
    # counting the new data to store to display them in the log
    # provider - the service that offer data
    provider_token = service.provider.token
    service_provider = default_provider.get_service(
        str(service.provider.name.name))

    # check if the service has already been triggered
    # if date_triggered is None, then it's the first run
    if service.date_triggered is None:
        logger.debug("first time {}".format(service))
        to_update = True
        # run run run
    else:
        # 1) get the data from the provider service
        # get a timestamp of the last triggered of the service
        kw = {'token': provider_token,
              'trigger_id': service.id,
              'date_triggered': service.date_triggered}
        getattr(service_provider, '__init__')(provider_token)
        data = getattr(service_provider, 'read_data')(**kw)
        # counting the new data to store to display them in the log
        count_new_data = len(data) if data else 0
        if count_new_data > 0:
            to_update = True

    if to_update:
        logger.info("{} - {} new data".format(service, count_new_data))
