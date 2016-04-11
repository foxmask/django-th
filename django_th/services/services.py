# coding: utf-8 -*-
# Using OAuth1Session
from requests_oauthlib import OAuth1Session

# django stuff
from django.core.cache import caches
from django.core.urlresolvers import reverse

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

# django_th stuff
from django_th.models import UserService, ServicesActivated
from django_th.publishing_limit import PublishingLimit
from django_th.html_entities import HtmlEntities


class ServicesMgr(object):
    """
        Main Service Class
    """
    name = ''
    title = ''
    body = ''
    data = {}

    class __ServicesMgr:

        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        base = 'https://www.urltotheserviceapi.com'
        self.AUTH_URL = '{}/api/rest/v1/oauth/authorize/'.format(base)
        self.REQ_TOKEN = '{}/api/rest/v1/oauth/request_token/'.format(base)
        self.ACC_TOKEN = '{}/api/rest/v1/oauth/access_token/'.format(base)

        if not ServicesMgr.instance:
            ServicesMgr.instance = ServicesMgr.__ServicesMgr(arg)
        else:
            ServicesMgr.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return self.name

    @staticmethod
    def _get_content(data, which_content):
        """
            get the content that could be hidden
            in the middle of "content" or "summary detail"
            from the data of the provider
        """
        content = ''
        if which_content in data:
            if type(data[which_content]) is list or\
               type(data[which_content]) is tuple or\
               type(data[which_content]) is dict:
                if 'value' in data[which_content][0]:
                    content = data[which_content][0].value
            else:
                if type(data[which_content]) is str:
                    content = data[which_content]
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data[which_content]['value']
        return content

    @staticmethod
    def set_title(data):
        """
            handle the title from the data
            :param data: contains the data from the provider
            :type data: dict
            :rtype: string
        """
        title = ''
        title = (data['title'] if 'title' in data else data['link'])

        return title

    def set_content(self, data):
        """
            handle the content from the data
            :param data: contains the data from the provider
            :type data: dict
            :rtype: string
        """
        content = self._get_content(data, 'content')

        if content == '':
            content = self._get_content(data, 'summary_detail')

        if content == '':
            if 'description' in data:
                content = data['description']

        return content

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id and model name
            :type kwargs: dict
            :rtype: model
        """
        model = get_model('django_th', kwargs['model_name'])

        return model.objects.get(trigger_id=kwargs['trigger_id'])

    def process_data(self, **kwargs):
        """
             get the data from the cache
            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
        """
        cache = caches[kwargs['cache_stack']]
        cache_data = cache.get(kwargs['cache_stack'] + '_' +
                               kwargs['trigger_id'])
        return PublishingLimit.get_data(kwargs['cache_stack'],
                                        cache_data, kwargs['trigger_id'])

    def save_data(self, trigger_id, data, **kwargs):
        """
            used to save data to the service
            but first of all
            make some work about the data to find
            and the data to convert
            :param trigger_id: trigger ID from which to save data
            :param data: the data to check to be used and save
            :type trigger_id: int
            :type data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        title = self.set_title(data)
        title = HtmlEntities(title).html_entity_decode
        content = self.set_content(data)
        content = HtmlEntities(content).html_entity_decode
        if 'output_format' in kwargs:
            # pandoc to convert tools
            import pypandoc
            content = pypandoc.convert(content,
                                       kwargs['output_format'],
                                       format='html')
        return title, content

    def auth(self, request):
        """
            get the auth of the services
            :param request: contains the current session
            :type request: dict
            :rtype: dict
        """
        request_token = self.get_request_token()

        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token[
            'oauth_token_secret']

        return request_token

    @staticmethod
    def callback_url(request, service):
        """
            the url to go back after the external service call
            :param request: contains the current session
            :param service: contains the service name
            :type request: dict
            :type service: string
            :rtype: string
        """
        return_to = '{service}_callback'.format(service=service)
        return 'http://%s%s' % (request.get_host(), reverse(return_to))

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            the url to go back after the external service call
            :param request: contains the current session
            :param kwargs: keyword args
            :type request: dict
            :type kwargs: dict
            :rtype: string
        """
        parms = ('access_token', 'service', 'return')
        if not all(k in parms for k in kwargs.keys()):
            raise KeyError('Missing args in kwargs. '
                           'Kwargs has to contains "access_token",'
                           ' "service" and "return"')

        if kwargs['access_token'] == '':
            access_token = self.get_access_token(
                request.session['oauth_token'],
                request.session['oauth_token_secret'],
                request.GET.get('oauth_verifier', '')
            )
        else:
            access_token = kwargs['access_token']

        if type(access_token) == str:
            token = access_token
        else:
            token = '#TH#'.join((access_token.get('oauth_token'),
                                 access_token.get('oauth_token_secret')))

        service_name = ServicesActivated.objects.get(name=kwargs['service'])

        UserService.objects.filter(user=request.user,
                                   name=service_name
                                   ).update(token=token)

        back_to = '{back_to}/callback.html'.format(back_to=kwargs['return'])
        return back_to

    def get_request_token(self):
        """
           request the token to the external service
        """
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret)
        return oauth.fetch_request_token(self.REQ_TOKEN)

    def get_access_token(self, oauth_token, oauth_token_secret,
                         oauth_verifier):
        """
           get the access token
            the url to go back after the external service call
            :param oauth_token: oauth token
            :param oauth_token_secret: oauth secret token
            :param oauth_verifier: oauth verifier
            :type oauth_token: string
            :type oauth_token_secret: string
            :type oauth_verifier: string
            :rtype: dict
        """
        # Using OAuth1Session
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=oauth_token,
                              resource_owner_secret=oauth_token_secret,
                              verifier=oauth_verifier)
        oauth_tokens = oauth.fetch_access_token(self.ACC_TOKEN)

        return oauth_tokens
