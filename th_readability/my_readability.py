# coding: utf-8
# oauth and url stuff

# Using OAuth1Session
from requests_oauthlib import OAuth1Session

# readability API
from readability import ReaderClient

# django classes
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated
from django_th.publishing_limit import PublishingLimit
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

    def __init__(self, token=None):
        base = 'https://www.readability.com'
        self.AUTH_URL = '{}/api/rest/v1/oauth/authorize/'.format(base)
        self.REQ_TOKEN = '{}/api/rest/v1/oauth/request_token/'.format(base)
        self.ACC_TOKEN = '{}/api/rest/v1/oauth/access_token/'.format(base)
        self.consumer_key = settings.TH_READABILITY['consumer_key']
        self.consumer_secret = settings.TH_READABILITY['consumer_secret']
        if token:
            token_key, token_secret = token.split('#TH#')
            self.client = ReaderClient(token_key, token_secret,
                                       self.consumer_key, self.consumer_secret)

    def read_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service

            :param trigger_id: trigger ID to process
            :param date_triggered: the date of the last trigger
            :type trigger_id: int
            :type date_triggered: datetime
            :return: list of data found from the date_triggered filter
            :rtype: list
        """
        data = []

        if token is not None:

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

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        cache_data = cache.get('th_readability_' + str(trigger_id))
        return PublishingLimit.get_data('th_readability_',
                                        cache_data,
                                        trigger_id)

    def save_data(self, token, trigger_id, **data):
        """
            let's save the data

            :param trigger_id: trigger ID from which to save data
            :param **data: the data to check to be used and save
            :type trigger_id: int
            :type **data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        status = False
        if token and 'link' in data and\
           data['link'] is not None and\
           len(data['link']) > 0:
            # get the data of this trigger
            trigger = Readability.objects.get(trigger_id=trigger_id)

            bookmark_id = self.client.add_bookmark(url=data['link'])

            if trigger.tag is not None and len(trigger.tag) > 0:
                try:
                    self.client.add_tags_to_bookmark(
                        bookmark_id, tags=(trigger.tag.lower()))
                    sentence = str('readability {} created item id {}').format(
                        data['link'], bookmark_id)
                    logger.debug(sentence)
                    status = True
                except Exception as e:
                    logger.critical(e)
                    status = False
        else:
            sentence = "no token or link provided for trigger ID {} "
            logger.critical(sentence.format(trigger_id))
            status = False

        return status

    def auth(self, request):
        """
            let's auth the user to the Service
        """
        callback_url = 'http://%s%s' % (
            request.get_host(), reverse('readability_callback'))

        request_token = self.get_request_token()

        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token[
            'oauth_token_secret']

        # URL to redirect user to, to authorize your app
        auth_url_str = '%s?oauth_token=%s&oauth_callback=%s'
        auth_url = auth_url_str % (self.AUTH_URL,
                                   request_token['oauth_token'],
                                   callback_url)

        return auth_url

    def callback(self, request):
        """
            Called from the Service when the user accept to activate it
        """

        try:
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous objet
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceReadability'))
            # 2) Readability API require to use 4 parms consumer_key/secret +
            # token_key/secret instead of usually get just the token
            # from an access_token request. So we need to add a string
            # seperator for later use to slpit on this one
            access_token = self.get_access_token(
                request.session['oauth_token'],
                request.session['oauth_token_secret'],
                request.GET.get('oauth_verifier', '')
            )
            us.token = access_token.get('oauth_token') + \
                '#TH#' + access_token.get('oauth_token_secret')

            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'readability/callback.html'

    def get_request_token(self):
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret)
        return oauth.fetch_request_token(self.REQ_TOKEN)

    def get_access_token(self, oauth_token, oauth_token_secret,
                         oauth_verifier):
        # Using OAuth1Session
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=oauth_token,
                              resource_owner_secret=oauth_token_secret,
                              verifier=oauth_verifier)
        oauth_tokens = oauth.fetch_access_token(self.ACC_TOKEN)

        return oauth_tokens
