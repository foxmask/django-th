# coding: utf-8
import arrow

# django classes
from django.conf import settings
from django.core.cache import caches
from django.core.urlresolvers import reverse
from logging import getLogger

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import update_result, UserService

from praw import Reddit as RedditApi

from th_reddit.models import Reddit


"""
put the following in settings.py
TH_REDDIT_KEY = {
    'client_id': 'abcdefghijklmnopqrstuvwxyz',
    'client_secret': 'abcdefghijklmnopqrstuvwxyz',
    'user_agent': '<platform>:<app ID>:<version> (by /u/<reddit username>)'
}

TH_SERVICES = (
    ...
    'th_reddit.my_reddit.ServiceReddit',
    ...
)
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['django_th']


class ServiceReddit(ServicesMgr):
    """
        service Reddit
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceReddit, self).__init__(token, **kwargs)
        self.consumer_key = settings.TH_REDDIT_KEY['client_id']
        self.consumer_secret = settings.TH_REDDIT_KEY['client_secret']
        self.user_agent = settings.TH_REDDIT_KEY['user_agent']
        self.service = 'ServiceReddit'
        self.oauth = 'oauth2'
        if token:
            self.token = token
            self.reddit = RedditApi(client_id=self.consumer_key,
                                    client_secret=self.consumer_secret,
                                    refresh_token=self.token,
                                    user_agent=self.user_agent)

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
        trigger = Reddit.objects.get(trigger_id=trigger_id)
        date_triggered = kwargs.get('date_triggered')
        data = list()
        submissions = self.reddit.subreddit(trigger.subreddit).top('all')
        for submission in submissions:
            title = 'From Reddit ' + submission.title
            created = arrow.get(submission.created)
            if created > date_triggered and submission.selftext is not None \
                    and trigger.share_link:
                body = submission.selftext if submission.selftext \
                    else submission.url
                data.append({'title': title, 'content': body})
                self.send_digest_event(trigger_id, title, '')

        cache.set('th_reddit_' + str(trigger_id), data)
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
        # convert the format to be released in Markdown
        status = False
        data['output_format'] = 'md'
        title, content = super(ServiceReddit, self).save_data(trigger_id,
                                                              **data)
        if self.token:

            trigger = Reddit.objects.get(trigger_id=trigger_id)
            if trigger.share_link:
                status = self.reddit.subreddit(trigger.subreddit)\
                    .submit(title=title, url=content)
            else:
                status = self.reddit.subreddit(trigger.subreddit)\
                    .submit(title=title, selftext=content)
            sentence = str('reddit submission {} created').format(title)
            logger.debug(sentence)
        else:
            msg = "no token or link provided for trigger " \
                  "ID {} ".format(trigger_id)
            logger.critical(msg)
            update_result(trigger_id, msg=msg, status=False)
        return status

    def auth(self, request):
        """

        :param request:
        :return:
        """
        redirect_uri = '%s://%s%s' % (request.scheme, request.get_host(),
                                      reverse("reddit_callback"))
        reddit = RedditApi(client_id=self.consumer_key,
                           client_secret=self.consumer_secret,
                           redirect_uri=redirect_uri,
                           user_agent=self.user_agent)
        auth_url = reddit.auth.url(['identity', 'read', 'submit', 'save'],
                                   'redirect_uri')
        return auth_url

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
        code = request.GET.get('code', '')
        redirect_uri = '%s://%s%s' % (request.scheme, request.get_host(),
                                      reverse("reddit_callback"))
        reddit = RedditApi(client_id=self.consumer_key,
                           client_secret=self.consumer_secret,
                           redirect_uri=redirect_uri,
                           user_agent=self.user_agent)

        token = reddit.auth.authorize(code)

        UserService.objects.filter(user=request.user,
                                   name='ServiceReddit'
                                   ).update(token=token)

        return 'reddit/callback.html'
