# coding: utf-8
import arrow
from logging import getLogger

from mastodon import Mastodon as MastodonAPI

# django classes
from django.conf import settings
from django.core.cache import caches
from django.shortcuts import reverse
from django.utils import html
from django.utils.translation import ugettext as _

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import update_result, UserService
from django_th.tools import download_image
from th_mastodon.models import Mastodon

import re

logger = getLogger('django_th.trigger_happy')

cache = caches['django_th']


class ServiceMastodon(ServicesMgr):
    """
        Service Mastodon
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceMastodon, self).__init__(token, **kwargs)

        self.token = token
        self.service = 'ServiceMastodon'
        self.user = kwargs.get('user')

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
            :rtype: list
        """
        now = arrow.utcnow().to(settings.TIME_ZONE)
        my_toots = []
        search = {}
        since_id = None
        trigger_id = kwargs['trigger_id']
        date_triggered = arrow.get(kwargs['date_triggered'])

        def _get_toots(toot_api, toot_obj, search):
            """
                get the toots from mastodon and return the filters to use

                :param toot_obj: from Mastodon model
                :param search: filter used for MastodonAPI.search()
                :type toot_obj: Object ServiceMastodon
                :type search: dict
                :return: the filter named search, the toots
                :rtype: list
            """
            max_id = 0 if toot_obj.max_id is None else toot_obj.max_id
            since_id = 0 if toot_obj.since_id is None else toot_obj.since_id
            # get the toots for a given tag
            statuses = ''

            if toot_obj.tag:
                search['q'] = toot_obj.tag
                # do a search
                statuses = toot_api.search(**search)
                # just return the content of te statuses array
                statuses = statuses['statuses']

            # get the tweets from a given user
            elif toot_obj.tooter:
                search['id'] = toot_obj.tooter
                # call the user timeline and get his toot
                if toot_obj.fav:
                    statuses = toot_api.favourites(max_id=max_id,
                                                   since_id=since_id)
                else:
                    user_id = toot_api.account_search(q=toot_obj.tooter)
                    statuses = toot_api.account_statuses(
                        id=user_id[0]['id'], max_id=toot_obj.max_id,
                        since_id=toot_obj.since_id)

            return search, statuses

        if self.token is not None:
            kw = {'app_label': 'th_mastodon', 'model_name': 'Mastodon',
                  'trigger_id': trigger_id}
            toot_obj = super(ServiceMastodon, self).read_data(**kw)

            us = UserService.objects.get(token=self.token,
                                         name='ServiceMastodon')
            try:
                toot_api = MastodonAPI(
                    client_id=us.client_id,
                    client_secret=us.client_secret,
                    access_token=self.token,
                    api_base_url=us.host,
                )
            except ValueError as e:
                logger.error(e)
                update_result(trigger_id, msg=e, status=False)

            if toot_obj.since_id is not None and toot_obj.since_id > 0:
                since_id = toot_obj.since_id
                search = {'since_id': toot_obj.since_id}

            # first request to Mastodon
            search, statuses = _get_toots(toot_api, toot_obj, search)

            if len(statuses) > 0:
                newest = None
                for status in statuses:
                    if newest is None:
                        newest = True
                        # first query ; get the max id
                        search['max_id'] = max_id = status['id']

                since_id = search['since_id'] = statuses[-1]['id'] - 1

                search, statuses = _get_toots(toot_api, toot_obj, search)

                newest = None
                if len(statuses) > 0:
                    my_toots = []
                    for s in statuses:
                        if newest is None:
                            newest = True
                            max_id = s['id'] - 1
                        toot_name = s['account']['username']
                        # get the text of the tweet + url to this one

                        title = _('Toot from <a href="{}">@{}</a>'.
                                  format(us.host, toot_name))

                        my_date = arrow.get(s['created_at']).to(
                            settings.TIME_ZONE)
                        published = arrow.get(my_date).to(settings.TIME_ZONE)
                        if date_triggered is not None and \
                           published is not None and \
                           now >= published >= date_triggered:
                            my_toots.append({'title': title,
                                             'content': s['content'],
                                             'link': s['url'],
                                             'my_date': my_date})
                            # digester
                            self.send_digest_event(trigger_id, title, s['url'])
                    cache.set('th_mastodon_' + str(trigger_id), my_toots)
                    Mastodon.objects.filter(trigger_id=trigger_id).update(
                        since_id=since_id, max_id=max_id)
        return my_toots

    def save_data(self, trigger_id, **data):
        """
            get the data from the service

            :param trigger_id: id of the trigger
            :params data, dict
            :rtype: dict
        """
        title, content = super(ServiceMastodon, self).save_data(
            trigger_id, **data)

        # check if we have a 'good' title
        if self.title_or_content(title):

            content = str("{title} {link}").format(title=title,
                                                   link=data.get('link'))
            content += self.get_tags(trigger_id)
        # if not then use the content
        else:
            content += " " + data.get('link')
            content += " " + self.get_tags(trigger_id)

        content = self.set_mastodon_content(content)

        us = UserService.objects.get(user=self.user,
                                     token=self.token,
                                     name='ServiceMastodon')

        try:
            toot_api = MastodonAPI(
                    client_id=us.client_id,
                    client_secret=us.client_secret,
                    access_token=self.token,
                    api_base_url=us.host
            )
        except ValueError as e:
            logger.error(e)
            status = False
            update_result(trigger_id, msg=e, status=status)

        media_ids = None
        try:
            if settings.DJANGO_TH['sharing_media']:
                # do we have a media in the content ?
                content, media = self.media_in_content(content)
                if media:
                    # upload the media first
                    media_ids = toot_api.media_post(media_file=media)
                    media_ids = [media_ids]

            toot_api.status_post(content, media_ids=media_ids)

            status = True
        except Exception as inst:
            logger.critical("Mastodon ERR {}".format(inst))
            status = False
            update_result(trigger_id, msg=inst, status=status)
        return status

    def get_tags(self, trigger_id):
        """
        get the tags if any
        :param trigger_id: the id of the related trigger
        :return: tags string
        """

        # get the Mastodon data of this trigger
        trigger = Mastodon.objects.get(trigger_id=trigger_id)

        tags = ''

        if trigger.tag is not None:
            # is there several tag ?
            tags = ["#" + tag.strip() for tag in trigger.tag.split(',')
                    ] if ',' in trigger.tag else "#" + trigger.tag

            tags = str(','.join(tags)) if isinstance(tags, list) else tags
            tags = ' ' + tags

        return tags

    def title_or_content(self, title):
        """
        If the title always contains 'Tweet from'
        drop the title and get 'the content' instead
        this allow to have a complet content and not
        just a little piece of string
        :param title:
        :return:
        """
        return "Tweet from" not in title

    def media_in_content(self, content):
        """
        check if the content contains and url of an image
        for the moment, check twitter media url
        could be elaborate with other service when needed
        :param content:
        :return:
        """
        local_file = ''
        if 'https://t.co' in content:
            content = re.sub(r'https://t.co/(\w+)', '', content)
        if 'https://pbs.twimg.com/media/' in content:
            m = re.search('https://pbs.twimg.com/media/([\w\-_]+).jpg', content)
            url = 'https://pbs.twimg.com/media/{}.jpg'.format(m.group(1))
            local_file = download_image(url)
            content = re.sub(r'https://pbs.twimg.com/media/([\w\-_]+).jpg', '',
                             content)

            return content, local_file
        return content, local_file

    def set_mastodon_content(self, content):
        """
        cleaning content by removing any existing html tag
        :param content:
        :return:
        """
        content = html.strip_tags(content)

        return content[:560] if len(content) > 560 else content

    def auth(self, request):
        """
            get the auth of the services
            :param request: contains the current session
            :type request: dict
            :rtype: dict
        """
        # create app
        redirect_uris = '%s://%s%s' % (request.scheme, request.get_host(),
                                       reverse('mastodon_callback'))
        us = UserService.objects.get(user=request.user,
                                     name='ServiceMastodon')
        client_id, client_secret = MastodonAPI.create_app(
            client_name="TriggerHappy", api_base_url=us.host,
            redirect_uris=redirect_uris)

        us.client_id = client_id
        us.client_secret = client_secret
        us.save()

        us = UserService.objects.get(user=request.user,
                                     name='ServiceMastodon')
        # get the token by logging in
        mastodon = MastodonAPI(
            client_id=client_id,
            client_secret=client_secret,
            api_base_url=us.host
        )
        token = mastodon.log_in(username=us.username, password=us.password)
        us.token = token
        us.save()
        return self.callback_url(request)

    def callback_url(self, request):
        us = UserService.objects.get(user=request.user,
                                     name='ServiceMastodon')
        mastodon = MastodonAPI(
            client_id=us.client_id,
            client_secret=us.client_secret,
            access_token=us.token,
            api_base_url=us.host
        )
        redirect_uris = '%s://%s%s' % (request.scheme, request.get_host(),
                                       reverse('mastodon_callback'))
        return mastodon.auth_request_url(redirect_uris=redirect_uris)

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
        return 'mastodon/callback.html'
