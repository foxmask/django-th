# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import

import arrow

# django
from django.conf import settings
from django.utils.log import getLogger

# trigger happy
from django_th.services import default_provider
from django_th.models import TriggerService, update_result


logger = getLogger('django_th.trigger_happy')

default_provider.load_services()


class Pub(object):
    """
        Publishing data to any service
    """

    def update_trigger(self, service):
        """
            update the date when occurs the trigger
            :param service: service object to update
        """
        now = arrow.utcnow().to(settings.TIME_ZONE).format(
            'YYYY-MM-DD HH:mm:ssZZ')
        TriggerService.objects.filter(id=service.id).update(date_triggered=now)

    def log_update(self, service, to_update, status, count):
        """
            lets log everything at the end
            :param service: service object
            :param to_update: boolean to check if we have to update
            :param status: is everything worked fine ?
            :param count: number of data to update
            :type service: service object
            :type to_update: boolean
            :type status: boolean
            :type count: interger
        """
        if to_update:
            if status:
                msg = "{} - {} new data".format(service, count)
                update_result(service.id, msg="OK")
                logger.info(msg)
            else:
                msg = "{} AN ERROR OCCURS ".format(service)
                update_result(service.id, msg=msg)
                logger.warn(msg)
        else:
            logger.debug("{} nothing new ".format(service))

    def provider(self, service):
        """
            get the data from (the cache of) the service provider
            :param service:
            :return: data
        """
        service_provider = default_provider.get_service(
            str(service.provider.name.name))

        # 1) get the data from the provider service
        module_name = 'th_' + \
                      service.provider.name.name.split('Service')[1].lower()
        kwargs = {'trigger_id': str(service.id), 'cache_stack': module_name}
        return getattr(service_provider, 'process_data')(**kwargs)

    def consumer(self, service, data, to_update, status):
        """
            call the consumer and handle the data
            :param service:
            :param data:
            :param to_update:
            :param status:
            :return: status
        """
        # consumer - the service which uses the data
        service_consumer = default_provider.get_service(
            str(service.consumer.name.name))
        kwargs = {'user': service.user}
        getattr(service_consumer, '__init__')(service.consumer.token,
                                              **kwargs)
        instance = getattr(service_consumer, 'save_data')

        # 2) for each one
        for d in data:
            d['userservice_id'] = service.consumer.id
            # the consumer will save the data and return if success or not
            status = instance(service.id, **d)

            to_update = True

        return to_update, status

    def publishing(self, service):
        """
            the purpose of this tasks is to get the data from the cache
            then publish them
            :param service: service object where we will publish
            :type service: object
        """
        # flag to know if we have to update
        to_update = False
        # flag to get the status of a service
        status = False
        # provider - the service that offer data
        # check if the service has already been triggered
        # if date_triggered is None, then it's the first run
        if service.date_triggered is None:
            logger.debug("first run {}".format(service))
            to_update = True
            status = True
        # run run run
        data = self.provider(service)
        count_new_data = len(data) if data else 0
        if count_new_data > 0:
            to_update, status = self.consumer(service, data, to_update, status)
            # let's log
        self.log_update(service, to_update, status, count_new_data)
        # let's update
        if to_update and status:
            self.update_trigger(service)
