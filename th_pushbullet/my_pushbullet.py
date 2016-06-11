# coding: utf-8

# Oauth2Session
from requests_oauthlib import OAuth2Session

# Pushbullet
from pushbullet import Pushbullet as Pushb

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.models import UserService, ServicesActivated
from django_th.services.services import ServicesMgr
from th_pushbullet.models import Pushbullet


"""
    handle process with pushbullet
    put the following in settings.py

    TH_PUSHBULLET = {
        'client_id': 'abcdefghijklmnopqrstuvwxyz',
        'client_secret': 'abcdefghijklmnopqrstuvwxyz',
    }
    TH_SERVICES = (
        ...
        'th_pushbullet.my_pushbullet.ServicePushbullet',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_pushbullet']


class ServicePushbullet(ServicesMgr):

    def __init__(self, token=None, **kwargs):
        super(ServicePushbullet, self).__init__(token, **kwargs)
        self.AUTH_URL = 'https://pushbullet.com/authorize'
        self.ACC_TOKEN = 'https://pushbullet.com/access_token'
        self.REQ_TOKEN = 'https://api.pushbullet.com/oauth2/token'
        self.consumer_key = settings.TH_PUSHBULLET['client_id']
        self.consumer_secret = settings.TH_PUSHBULLET['client_secret']
        self.scope = 'everything'
        if token:
            self.token = token
            self.pushb = Pushb(token)

    def read_data(self, **kwargs):
        """
            get the data from the service
            as the pushbullet service does not have any date
            in its API linked to the note,
            add the triggered date to the dict data
            thus the service will be triggered when data will be found

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict

            :rtype: list
        """
        trigger_id = kwargs['trigger_id']
        data = list()
        cache.set('th_pushbullet_' + str(trigger_id), data)

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

        title, content = super(ServicePushbullet, self).save_data(trigger_id,
                                                                  data,
                                                                  **kwargs)

        if self.token:
            trigger = Pushbullet.objects.get(trigger_id=trigger_id)
            if trigger.type == 'note':
                status = self.pushb.push_note(title=title, body=content)
            elif trigger.type == 'link':
                status = self.pushb.push_link(title=title, body=content,
                                              url=data.get('link'))
                sentence = str('pushbullet {} created').format(title)
                logger.debug(sentence)
            else:
                # no valid type of pushbullet specified
                logger.critical("no valid type of pushbullet specified")
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
        callback_url = self.callback_url(request, 'pushbullet')
        oauth = OAuth2Session(client_id=self.consumer_key,
                              redirect_uri=callback_url)
        authorization_url, state = oauth.authorization_url(self.AUTH_URL)

        return authorization_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
        """
        callback_url = self.callback_url(request, 'pushbullet')
        oauth = OAuth2Session(client_id=self.consumer_key,
                              scope=self.scope,
                              redirect_uri=callback_url)
        response = oauth.fetch_token(self.REQ_TOKEN,
                                     code=request.GET.get('code', ''),
                                     authorization_response=callback_url,
                                     client_secret=self.consumer_secret)

        token = response.get('access_token')
        service_name = ServicesActivated.objects.get(name='ServicePushbullet')
        UserService.objects.filter(user=request.user,
                                   name=service_name
                                   ).update(token=token)

        return 'pushbullet/callback.html'
