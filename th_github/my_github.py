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

    def read_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service
            as the pocket service does not have any date
            in its API linked to the note,
            add the triggered date to the dict data
            thus the service will be triggered when data will be found
            :param trigger_id: trigger ID to process
            :param date_triggered: the date of the last trigger
            :type trigger_id: int
            :type date_triggered: datetime
            :return: list of data found from the date_triggered filter
            :rtype: list
        """
        data = list()
        cache.set('th_github_' + str(trigger_id), data)

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        datas = list()
        return datas

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
        from th_github.models import Github
        status = False

        if token:
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
                # rate limite reach
                logger.warn("Rate limit reached")
                # put again in cache the data that could not be
                # published in Github yet
                cache.set('th_github_' + str(trigger_id), data, version=2)
                return True
            sentance = str('github {} created').format(r)
            logger.debug(sentance)
            status = True
        else:
            logger.critical(
                "no token or link provided for trigger ID {} ".format(trigger_id))
            status = False

        return status

    def auth(self, request):
        """
            let's auth the user to the Service
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
                name=ServicesActivated.objects.get(name='ServiceGithub'))
            # 2) Readability API require to use 4 parms consumer_key/secret +
            # token_key/secret instead of usually get just the token
            # from an access_token request. So we need to add a string
            # seperator for later use to slpit on this one
            access_token = request.session['oauth_token'] + "#TH#" + str(request.session['oauth_id'])
            us.token = access_token
            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'github/callback.html'
