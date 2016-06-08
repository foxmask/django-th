# coding: utf-8

# Oauth2Session
from requests_oauthlib import OAuth2Session

# TodoistAPI
from todoist import TodoistAPI

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.models import UserService, ServicesActivated
from django_th.services.services import ServicesMgr


"""
    handle process with todoist
    put the following in settings.py

    TH_TODOIST = {
        'client_id': 'abcdefghijklmnopqrstuvwxyz',
        'client_secret': 'abcdefghijklmnopqrstuvwxyz',
    }
    TH_SERVICES = (
        ...
        'th_todoist.my_todoist.ServiceTodoist',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_todoist']


class ServiceTodoist(ServicesMgr):

    def __init__(self, token=None, **kwargs):
        super(ServiceTodoist, self).__init__(token, **kwargs)
        self.AUTH_URL = 'https://todoist.com/oauth/authorize'
        self.ACC_TOKEN = 'https://todoist.com/oauth/access_token'
        self.REQ_TOKEN = 'https://todoist.com/oauth/authorize'
        self.consumer_key = settings.TH_TODOIST['client_id']
        self.consumer_secret = settings.TH_TODOIST['client_secret']
        self.scope = 'task:add,data:read,data:read_write'
        if token:
            self.token = token
            self.todoist = TodoistAPI(token)

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
        trigger_id = kwargs['trigger_id']
        data = list()
        cache.set('th_todoist_' + str(trigger_id), data)

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
        kwargs = {}

        title, content = super(ServiceTodoist, self).save_data(trigger_id,
                                                               data, **kwargs)

        if self.token:
            if title or content or \
                            (data.get('link') and len(data.get('link'))) > 0:
                content = title + ' ' + content + ' ' + data.get('link')

                self.todoist.add_item(content)

                sentence = str('todoist {} created').format(data.get('link'))
                logger.debug(sentence)
                status = True
            else:
                status = False
        else:
            logger.critical("no token or link provided for "
                            "trigger ID {} ".format(trigger_id))
            status = False
        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        callback_url = self.callback_url(request, 'todoist')
        oauth = OAuth2Session(client_id=self.consumer_key,
                              redirect_uri=callback_url,
                              scope=self.scope)
        authorization_url, state = oauth.authorization_url(self.AUTH_URL)

        return authorization_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
        """
        callback_url = self.callback_url(request, 'todoist')
        oauth = OAuth2Session(client_id=self.consumer_key,
                              redirect_uri=callback_url,
                              scope=self.scope)
        request_token = oauth.fetch_token(self.ACC_TOKEN,
                                          code=request.GET.get('code', ''),
                                          authorization_response=callback_url,
                                          client_secret=self.consumer_secret)
        token = request_token.get('access_token')
        service_name = ServicesActivated.objects.get(name='ServiceTodoist')
        UserService.objects.filter(user=request.user,
                                   name=service_name
                                   ).update(token=token)

        return 'todoist/callback.html'
