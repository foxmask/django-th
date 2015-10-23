# -*- coding: utf-8 -*-
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
        return "%s" % self.name

    def _get_content(self, data, which_content):
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

    def set_title(self, data):
        """
            handle the title from the data
        """
        title = ''
        title = (data['title'] if 'title' in data else data['link'])

        return title

    def set_content(self, data):
        """
            handle the content from the data
        """
        content = ''
        content = self._get_content(data, 'content')

        if content == '':
            content = self._get_content(data, 'summary_detail')

        if content == '':
            if 'description' in data:
                content = data['description']

        return content

    def read_data(self, model_name, trigger_id):
        """
            get the data details from the service
        """
        model = get_model('django_th', model_name)

        return model.objects.get(trigger_id=trigger_id)

    def process_data(self, cache_stack, trigger_id):
        """
            used to get data from the service

            :param cache_stack: contains the name of the module eg th_twitter,
            th_evernote and so on
            :type cache_stack: string
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: string
            :return cache data
            :rtype dict
        """
        cache = caches[cache_stack]
        cache_data = cache.get(cache_stack + '_' + trigger_id)
        return PublishingLimit.get_data(cache_stack, cache_data, trigger_id)

    def save_data(self, data, **kwargs):
        """
            used to save data to the service
            but first of all
            make some work about the data to find
            and the data to convert
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
        """
        request_token = self.get_request_token()

        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token[
            'oauth_token_secret']

        return request_token

    def callback_url(self, request, service):
        return_to = '{service}_callback'.format(service=service)
        return 'http://%s%s' % (request.get_host(), reverse(return_to))

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
        """
        parms = ('access_token', 'service', 'return')
        if not all(k in parms for k in kwargs.keys()):
            raise KeyError('Missing args in kwargs. Kwargs has to contains "access_token", "service" and "return"')

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
