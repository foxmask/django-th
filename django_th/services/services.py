# coding: utf-8
# Using OAuth1Session
from requests_oauthlib import OAuth1Session, OAuth2Session

# django stuff
from django.core.cache import caches
from django.core.urlresolvers import reverse
from django.conf import settings

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

# django_th stuff
from django_th import signals
from django_th.models import UserService, ServicesActivated, TriggerService
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

    class __ServicesMgr:  # NOQA

        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg, **kwargs):
        base = 'https://www.urltotheserviceapi.com'
        self.AUTH_URL = '{}/api/rest/v1/oauth/authorize/'.format(base)
        self.REQ_TOKEN = '{}/api/rest/v1/oauth/request_token/'.format(base)
        self.ACC_TOKEN = '{}/api/rest/v1/oauth/access_token/'.format(base)
        self.oauth = 'oauth1'
        self.token = ''
        self.service = ''
        self.scope = ''
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
        if data.get(which_content):
            if type(data.get(which_content)) is list or\
               type(data.get(which_content)) is tuple or\
               type(data.get(which_content)) is dict:
                if 'value' in data.get(which_content)[0]:
                    content = data.get(which_content)[0].value
            else:
                if type(data.get(which_content)) is str:
                    content = data.get(which_content)
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data.get(which_content)['value']
        return content

    @staticmethod
    def set_title(data):
        """
            handle the title from the data
            :param data: contains the data from the provider
            :type data: dict
            :rtype: string
        """
        title = (data.get('title') if data.get('title') else data.get('link'))

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
            if data.get('description'):
                content = data.get('description')

        return content

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id and model name
            :type kwargs: dict
            :rtype: model
        """
        model = get_model(kwargs['app_label'], kwargs['model_name'])

        return model.objects.get(trigger_id=kwargs['trigger_id'])

    def process_data(self, **kwargs):
        """
             get the data from the cache
            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
        """
        cache = caches['django_th']
        cache_data = cache.get(kwargs.get('cache_stack') + '_' +
                               kwargs.get('trigger_id'))
        return PublishingLimit.get_data(kwargs.get('cache_stack'),
                                        cache_data,
                                        int(kwargs.get('trigger_id')))

    def save_data(self, trigger_id, **data):
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
        if data.get('output_format'):
            # pandoc to convert tools
            import pypandoc
            content = pypandoc.convert(content,
                                       str(data.get('output_format')),
                                       format='html')
        return title, content

    def auth(self, request):
        """
            get the auth of the services
            :param request: contains the current session
            :type request: dict
            :rtype: dict
        """
        request_token = self.get_request_token(request)

        return request_token

    def callback_url(self, request):
        """
            the url to go back after the external service call
            :param request: contains the current session
            :type request: dict
            :rtype: string
        """
        service = self.service.split('Service')[1].lower()
        return_to = '{service}_callback'.format(service=service)
        return '%s://%s%s' % (request.scheme, request.get_host(),
                              reverse(return_to))

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
        if self.oauth == 'oauth1':
            token = self.callback_oauth1(request, **kwargs)
        else:
            token = self.callback_oauth2(request)

        service_name = ServicesActivated.objects.get(name=self.service)

        UserService.objects.filter(user=request.user,
                                   name=service_name
                                   ).update(token=token)
        back = self.service.split('Service')[1].lower()
        back_to = '{back_to}/callback.html'.format(back_to=back)
        return back_to

    def callback_oauth1(self, request, **kwargs):
        """
            Process for oAuth 1
            :param request: contains the current session
            :param kwargs: keyword args
            :type request: dict
            :type kwargs: dict
            :rtype: string
        """
        if kwargs.get('access_token') == '' \
           or kwargs.get('access_token') is None:
            access_token = self.get_access_token(
                request.session['oauth_token'],
                request.session['oauth_token_secret'],
                request.GET.get('oauth_verifier', '')
            )
        else:
            access_token = kwargs.get('access_token')

        if type(access_token) == str:
            token = access_token
        else:
            token = '#TH#'.join((access_token.get('oauth_token'),
                                 access_token.get('oauth_token_secret')))
        return token

    def callback_oauth2(self, request):
        """
            Process for oAuth 2
            :param request: contains the current session
            :return:
        """
        callback_url = self.callback_url(request)

        oauth = OAuth2Session(client_id=self.consumer_key,
                              redirect_uri=callback_url,
                              scope=self.scope)
        request_token = oauth.fetch_token(self.REQ_TOKEN,
                                          code=request.GET.get('code', ''),
                                          authorization_response=callback_url,
                                          client_secret=self.consumer_secret,
                                          scope=self.scope,
                                          verify=False)
        return request_token.get('access_token')

    def get_request_token(self, request):
        """
           request the token to the external service
        """
        if self.oauth == 'oauth1':
            oauth = OAuth1Session(self.consumer_key,
                                  client_secret=self.consumer_secret)
            request_token = oauth.fetch_request_token(self.REQ_TOKEN)
            # Save the request token information for later
            request.session['oauth_token'] = request_token['oauth_token']
            request.session['oauth_token_secret'] = request_token[
                'oauth_token_secret']

            return request_token
        else:
            callback_url = self.callback_url(request)
            oauth = OAuth2Session(client_id=self.consumer_key,
                                  redirect_uri=callback_url,
                                  scope=self.scope)
            authorization_url, state = oauth.authorization_url(self.AUTH_URL)
            return authorization_url

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

    def reset_failed(self, pk):
        """
            reset failed counter
        :param pk:
        :return:
        """
        TriggerService.objects.filter(consumer__name__id=pk).update(
            consumer_failed=0, provider_failed=0)
        TriggerService.objects.filter(provider__name__id=pk).update(
            consumer_failed=0, provider_failed=0)

    def send_digest_event(self, trigger_id, title, link=''):
        """
        handling of the signal of digest
        :param trigger_id:
        :param title:
        :param link:
        :return:
        """
        if settings.DJANGO_TH.get('digest_event'):

            t = TriggerService.objects.get(id=trigger_id)

            if t.provider.duration != 'n':

                kwargs = {'user': t.user, 'title': title,
                          'link': link, 'duration': t.provider.duration}

                signals.digest_event.send(sender=t.provider.name, **kwargs)
