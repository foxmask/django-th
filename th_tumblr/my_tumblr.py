# coding: utf-8
from pytumblr import TumblrRestClient
# django classes
from django.conf import settings
from django.core.cache import caches

from logging import getLogger

# django_th classes
from django_th.services.services import ServicesMgr

"""
    handle process with tumblr
    put the following in th_settings.py

    TH_TUMBLR = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',

    }
"""

logger = getLogger('django_th.trigger_happy')
cache = caches['django_th']


class ServiceTumblr(ServicesMgr):
    """
        Service Tumblr
    """
    def __init__(self, token=None, **kwargs):
        """

        :param token:
        :param kwargs:
        """
        super(ServiceTumblr, self).__init__(token, **kwargs)
        self.AUTH_URL = 'https://www.tumblr.com/oauth/authorize'
        self.ACC_TOKEN = 'https://www.tumblr.com/oauth/access_token'
        self.REQ_TOKEN = 'https://www.tumblr.com/oauth/request_token'
        self.consumer_key = settings.TH_TUMBLR_KEY['consumer_key']
        self.consumer_secret = settings.TH_TUMBLR_KEY['consumer_secret']
        self.token = token
        self.service = 'ServiceTumblr'
        self.oauth = 'oauth1'
        if self.token is not None:
            token_key, token_secret = self.token.split('#TH#')

            self.tumblr = TumblrRestClient(self.consumer_key,
                                           self.consumer_secret,
                                           token_key,
                                           token_secret)

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
        cache.set('th_tumblr_' + str(trigger_id), data)
        return data

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
        from th_tumblr.models import Tumblr

        title, content = super(ServiceTumblr, self).save_data(trigger_id,
                                                              **data)

        # get the data of this trigger
        trigger = Tumblr.objects.get(trigger_id=trigger_id)
        # we suppose we use a tag property for this service
        status = self.tumblr.create_text(blogname=trigger.blogname,
                                         title=title,
                                         body=content,
                                         state='published',
                                         tags=trigger.tag)

        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        request_token = super(ServiceTumblr, self).auth(request)
        callback_url = self.callback_url(request)

        # URL to redirect user to, to authorize your app
        auth_url_str = '{auth_url}?oauth_token={token}'
        auth_url_str += '&oauth_callback={callback_url}'
        auth_url = auth_url_str.format(auth_url=self.AUTH_URL,
                                       token=request_token['oauth_token'],
                                       callback_url=callback_url)

        return auth_url
