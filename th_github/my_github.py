# coding: utf-8
# github
from github3 import GitHub

# django classes
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated

"""
    handle process with github
    put the following in settings.py

    TH_GITHUB = {
        'username': 'username',
        'password': 'password',
        'consumer_key': 'my key',
        'consumer_secret': 'my secret'
    }


    TH_SERVICES = (
        ...
        'th_github.my_github.ServiceGithub',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_github']


class ServiceGithub(ServicesMgr):

    def __init__(self, token=None):
        super(ServiceGithub, self).__init__(token)
        self.scope = ['public_repo']
        self.REQ_TOKEN = 'https://github.com/login/oauth/authorize'
        self.AUTH_URL = 'https://github.com/login/oauth/authorize'
        self.ACC_TOKEN = 'https://github.com/login/oauth/access_token'
        self.username = settings.TH_GITHUB['username']
        self.password = settings.TH_GITHUB['password']
        self.consumer_key = settings.TH_GITHUB['consumer_key']
        self.consumer_secret = settings.TH_GITHUB['consumer_secret']
        self.token = token
        if self.token:
            token_key, token_secret = self.token.split('#TH#')
            self.gh = GitHub(token=token_key)
        else:
            self.gh = GitHub(username=self.username, password=self.password)

    def read_data(self, **kwargs):
        """
            get the data from the service
            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
            :rtype: list
        """
        trigger_id = kwargs['trigger_id']
        data = list()
        cache.set('th_github_' + str(trigger_id), data)

    def process_data(self, **kwargs):
        """
            get the data from the cache
            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
        """
        kw = {'cache_stack': 'th_github',
              'trigger_id': str(kwargs['trigger_id'])}
        return super(ServiceGithub, self).process_data(**kw)

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
        from th_github.models import Github
        if self.token:
            title = self.set_title(data)
            body = self.set_content(data)
            # get the details of this trigger
            trigger = Github.objects.get(trigger_id=trigger_id)

            # check if it remains more than 1 access
            # then we can create an issue
            limit = self.gh.ratelimit_remaining
            if limit > 1:
                # repo goes to "owner"
                # project goes to "repository"
                r = self.gh.create_issue(trigger.repo,
                                         trigger.project,
                                         title,
                                         body)
            else:
                # rate limit reach
                logger.warn("Rate limit reached")
                # put again in cache the data that could not be
                # published in Github yet
                cache.set('th_github_' + str(trigger_id), data, version=2)
                return True
            sentence = str('github {} created').format(r)
            logger.debug(sentence)
            status = True
        else:
            sentence = "no token or link provided for trigger ID {} "
            logger.critical(sentence.format(trigger_id))
            status = False

        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        callback_url = 'http://%s%s' % (
            request.get_host(), reverse('github_callback'))
        auth = self.gh.authorize(self.username,
                                 self.password,
                                 self.scope,
                                 '',
                                 '',
                                 self.consumer_key,
                                 self.consumer_secret)
        request.session['oauth_token'] = auth.token
        request.session['oauth_id'] = auth.id
        return callback_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            :param request: request object
            :return: callback url
            :rtype: string , path to the template
        """
        try:
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous objet
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceGithub'))
            # 2) Readability API require to use 4 params consumer_key/secret +
            # token_key/secret instead of usually get just the token
            # from an access_token request. So we need to add a string
            # separator for later use to split on this one
            access_token = request.session['oauth_token'] + "#TH#"
            access_token += str(request.session['oauth_id'])
            us.token = access_token
            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'github/callback.html'
