# coding: utf-8
# add here the call of any native lib of python like datetime etc.

# add the python API here if needed
from praw import Reddit
# django classes
from django.core.cache import caches

from logging import getLogger

# django_th classes
from django_th.services.services import ServicesMgr


"""
    TH_SERVICES = (
        ...
        'th_reddit.my_reddit.ServiceReddit',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['django_th']


class ServiceReddit(ServicesMgr):

    def read_data(self, **kwargs):
        """
            get the data from the service
            as the pocket service does not have any date
            in its API linked to the note,
            add the triggered date to the dict data
            thus the service will be triggered when data will be found

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict

            :rtype: list
        """
        trigger_id = kwargs.get('trigger_id')
        data = list()
        cache.set('th_reddit_' + str(trigger_id), data)

    def save_data(self, trigger_id, **data):
        """
            let's save the data
            :param trigger_id: trigger ID from which to save data
            :param data: the data to check to be used and save
            :type trigger_id: int
            :type data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        from th_reddit.models import Reddit

        status = False

        title, content = super(ServiceReddit, self).save_data(trigger_id, **data)

        # get the data of this trigger
        trigger = Reddit.objects.get(trigger_id=trigger_id)
        # we suppose we use a tag property for this service
        status = self.reddit.add(title=title, content=content, tags= trigger.tags)

        return status

