# coding: utf-8
# add here the call of any native lib of python like datetime etc.

# add the python API here if needed
from joplin_api import JoplinApi
# django classes
from django.core.cache import caches
from django.conf import settings

from logging import getLogger

# django_th classes
from django_th.services.services import ServicesMgr


"""
    TH_SERVICES = (
        ...
        'th_joplin.my_joplin.ServiceJoplin',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['django_th']


class ServiceJoplin(ServicesMgr):

    def __init__(self, token=None, **kwargs):
        super(ServiceJoplin, self).__init__(token, **kwargs)
        self.token = settings.TH_JOPLIN_TOKEN
        self.user = kwargs.get('user')
        self.joplin = JoplinApi(token=self.token)

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
        cache.set('th_joplin_' + str(trigger_id), data)

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
        from th_joplin.models import Joplin

        status = False

        data['output_format'] = 'markdown_github'
        title, content = super(ServiceJoplin, self).save_data(trigger_id, **data)

        # get the data of this trigger
        trigger = Joplin.objects.get(trigger_id=trigger_id)
        status = self.joplin.create_note(title=title, body=content, parent_id=trigger.folder).status_code
        if status == 200:
            status = True
        return status
