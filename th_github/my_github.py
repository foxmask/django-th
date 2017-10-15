# coding: utf-8
# github
from github3 import GitHub

# django classes
from django.conf import settings
from logging import getLogger
from django.core.cache import caches
from django.utils.translation import ugettext as _

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import update_result
from th_github.models import Github

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

cache = caches['django_th']


class ServiceGithub(ServicesMgr):
    """
        Service Github
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceGithub, self).__init__(token, **kwargs)
        self.scope = ['public_repo']
        self.REQ_TOKEN = 'https://github.com/login/oauth/authorize'
        self.AUTH_URL = 'https://github.com/login/oauth/authorize'
        self.ACC_TOKEN = 'https://github.com/login/oauth/access_token'
        self.username = settings.TH_GITHUB_KEY['username']
        self.password = settings.TH_GITHUB_KEY['password']
        self.consumer_key = settings.TH_GITHUB_KEY['consumer_key']
        self.consumer_secret = settings.TH_GITHUB_KEY['consumer_secret']
        self.token = token
        self.oauth = 'oauth1'
        self.service = 'ServiceGithub'
        if self.token:
            token_key, token_secret = self.token.split('#TH#')
            self.gh = GitHub(token=token_key)
        else:
            self.gh = GitHub(username=self.username, password=self.password)

    def gh_footer(self, trigger, issue):

        link = 'https://github.com/{0}/{1}/issues/{2}'.format(
            trigger.repo, trigger.project, issue.id)

        provided_by = _('Provided by')
        provided_from = _('from')
        footer_from = "<br/><br/>{} <em>{}</em> {} <a href='{}'>{}</a>"

        return footer_from.format(provided_by, trigger.trigger.description,
                                  provided_from, link, link)

    def read_data(self, **kwargs):
        """
            get the data from the service
            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
            :rtype: list
        """
        trigger_id = kwargs.get('trigger_id')
        date_triggered = str(kwargs.get('date_triggered')).replace(' ', 'T')
        data = list()
        if self.token:
            # check if it remains more than 1 access
            # then we can create an issue
            if self.gh.ratelimit_remaining > 1:

                import pypandoc

                trigger = Github.objects.get(trigger_id=trigger_id)
                issues = self.gh.issues_on(trigger.repo,
                                           trigger.project,
                                           since=date_triggered)

                for issue in issues:

                    content = pypandoc.convert(issue.body, 'md', format='html')
                    content += self.gh_footer(trigger, issue)

                    data.append({'title': issue.title, 'content': content})
                    # digester
                    self.send_digest_event(trigger_id,
                                           issue.title,
                                           '')
                cache.set('th_github_' + str(trigger_id), data)
            else:
                # rate limit reach, do nothing right now
                logger.warning("Rate limit reached")
                update_result(trigger_id, msg="Rate limit reached",
                              status=True)
        else:
            logger.critical("no token provided")
            update_result(trigger_id, msg="No token provided", status=True)
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
                update_result(trigger_id, msg="Rate limit reached",
                              status=True)
                # put again in cache the data that could not be
                # published in Github yet
                cache.set('th_github_' + str(trigger_id), data, version=2)
                return True
            sentence = str('github {} created').format(r)
            logger.debug(sentence)
            status = True
        else:
            sentence = "no token or link provided for " \
                       "trigger ID {} ".format(trigger_id)
            logger.critical(sentence)
            update_result(trigger_id, msg=sentence, status=False)
            status = False

        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        auth = self.gh.authorize(self.username,
                                 self.password,
                                 self.scope,
                                 '',
                                 '',
                                 self.consumer_key,
                                 self.consumer_secret)
        request.session['oauth_token'] = auth.token
        request.session['oauth_id'] = auth.id
        return self.callback_url(request)

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            :param request: request object
            :return: callback url
            :rtype: string , path to the template
        """
        access_token = request.session['oauth_token'] + "#TH#"
        access_token += str(request.session['oauth_id'])
        kwargs = {'access_token': access_token}
        return super(ServiceGithub, self).callback(request, **kwargs)
