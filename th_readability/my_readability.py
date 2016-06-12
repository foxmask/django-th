# coding: utf-8
# readability API
from readability import ReaderClient

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from th_readability.models import Readability

"""
    handle process with readability
    put the following in settings.py

    TH_READABILITY = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }

    TH_SERVICES = (
        ...
        'th_readability.my_readability.ServiceReadability',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_readability']


class ServiceReadability(ServicesMgr):

    def __init__(self, token=None, **kwargs):
        super(ServiceReadability, self).__init__(token, **kwargs)
        base = 'https://www.readability.com'
        self.AUTH_URL = '{}/api/rest/v1/oauth/authorize/'.format(base)
        self.REQ_TOKEN = '{}/api/rest/v1/oauth/request_token/'.format(base)
        self.ACC_TOKEN = '{}/api/rest/v1/oauth/access_token/'.format(base)
        self.consumer_key = settings.TH_READABILITY['consumer_key']
        self.consumer_secret = settings.TH_READABILITY['consumer_secret']
        self.token = token
        self.service = 'ServiceReadability'
        self.oauth = 'oauth1'
        kwargs = {'consumer_key': self.consumer_key,
                  'consumer_secret': self.consumer_secret}
        if token:
            token_key, token_secret = self.token.split('#TH#')
            self.client = ReaderClient(token_key, token_secret, **kwargs)

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict

            :rtype: list
        """
        date_triggered = kwargs.get('date_triggered')
        trigger_id = kwargs.get('trigger_id')
        data = []

        if self.token is not None:

            bookmarks = self.client.get_bookmarks(
                added_since=date_triggered).content

            for bookmark in bookmarks.values():

                for b in bookmark:
                    if 'article' in b:
                        title = ''
                        if 'title' in b['article']:
                            title = b['article']['title']

                        link = ''
                        if 'url' in b['article']:
                            link = b['article']['url']

                        content = ''
                        if 'excerpt' in b['article']:
                            content = b['article']['excerpt']

                        data.append(
                            {'title': title,
                             'link': link,
                             'content': content})

            cache.set('th_readability_' + str(trigger_id), data)

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
        status = False
        if data.get('link'):
            if len(data.get('link')) > 0:
                # get the data of this trigger
                trigger = Readability.objects.get(trigger_id=trigger_id)

                bookmark_id = self.client.add_bookmark(url=data.get('link'))

                if trigger.tag is not None and len(trigger.tag) > 0:
                    try:
                        self.client.add_tags_to_bookmark(
                            bookmark_id, tags=(trigger.tag.lower()))
                        sentence = str('readability {} '
                                       'created item id {}').format(
                            data.get('link'), bookmark_id)
                        logger.debug(sentence)
                        status = True
                    except Exception as e:
                        logger.critical(e)
                        status = False

            else:
                logger.warning(
                    "no link provided for trigger ID {},"
                    " so we ignore it".format(trigger_id))
                status = True
        else:
            logger.critical(
                "no token provided for trigger ID {}".format(trigger_id))
            status = False
        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        request_token = super(ServiceReadability, self).auth(request)
        callback_url = self.callback_url(request)

        # URL to redirect user to, to authorize your app
        auth_url_str = '%s?oauth_token=%s&oauth_callback=%s'
        auth_url = auth_url_str % (self.AUTH_URL,
                                   request_token['oauth_token'],
                                   callback_url)

        return auth_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            :param request: request object
            :return: callback url
            :rtype: string , path to the template
        """
        return super(ServiceReadability, self).callback(request, **kwargs)
