# coding: utf-8
import requests

# django classes
from logging import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import TriggerService
from th_slack.models import Slack

logger = getLogger('django_th.trigger_happy')

cache = caches['django_th']


class ServiceSlack(ServicesMgr):
    """
        Service Slack
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceSlack, self).__init__(token, **kwargs)

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
        service = TriggerService.objects.get(id=trigger_id)
        desc = service.description

        slack = Slack.objects.get(trigger_id=trigger_id)

        title = self.set_title(data)
        if title is None:
            title = data.get('subject')
        type_action = data.get('type_action', '')

        # set the bot username of Slack to the name of the
        # provider service
        username = service.provider.name.name.split('Service')[1]
        # 'build' a link
        title_link = ''
        if data.get('permalink'):
            title_link = ': <' + data.get('permalink') + '|' + title + '>'
        else:
            title_link = ': <' + data.get('link') + '|' + title + '>'
            
        data = '*' + desc + '*: ' + type_action + title_link

        payload = {'username': username,
                   'text': data}

        r = requests.post(slack.webhook_url, json=payload)

        if r.status_code == requests.codes.ok:
            status = True
        # return the data
        return status
