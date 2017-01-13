# coding: utf-8
from taiga import TaigaAPI

# django classes
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService
from th_taiga.models import Taiga

logger = getLogger('django_th.trigger_happy')

cache = caches['th_taiga']


class ServiceTaiga(ServicesMgr):
    """
        Service Slack
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceTaiga, self).__init__(token, **kwargs)

        self.user = kwargs.get('user')

    def taiga_api(self):

        us = UserService.objects.get(user=self.user, name='ServiceTaiga')
        if us.token:
            api = TaigaAPI(token=us.token, host=us.host)
        else:
            api = TaigaAPI(host=us.host)
            api.auth(us.username, us.password)
        return api

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id and model name
            :type kwargs: dict
            :rtype: dict
        """
        data = ()
        return data

    def save_data(self, trigger_id, **data):
        """
            get the data from the service

            :param trigger_id: id of the trigger
            :params data, dict
            :rtype: dict
        """
        status = False
        taiga = Taiga.objects.get(trigger_id=trigger_id)
        title = self.set_title(data)
        body = self.set_content(data)
        # add a 'story' to the project
        if taiga.project_name:
            api = self.taiga_api()
            new_project = api.projects.get_by_slug(taiga.project_name)
            userstory = new_project.add_user_story(title, description=body)
            if userstory:
                status = True

        return status
