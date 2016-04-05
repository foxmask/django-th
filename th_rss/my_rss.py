# coding: utf-8
import datetime
import time
import arrow

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
# th_rss classes
from th_rss.lib.feedsservice import Feeds

logger = getLogger('django_th.trigger_happy')

cache = caches['ServiceRss']


class ServiceRss(ServicesMgr):

    def __init__(self, token=None):
        super(ServiceRss, self).__init__(token)

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id and model name
            :type kwargs: dict
            :rtype: dict
        """
        date_triggered = kwargs['date_triggered']
        trigger_id = kwargs['trigger_id']
        consumer = kwargs['consumer']
        consumer_token = kwargs['token']
        kwargs['model_name'] = 'Rss'

        # get the URL from the trigger id
        rss = super(ServiceRss, self).read_data(**kwargs)

        logger.debug("RSS Feeds from %s : url %s", rss.name, rss.url)

        now = arrow.utcnow().to(settings.TIME_ZONE)
        published = ''
        my_feeds = []

        # retrieve the data
        f = Feeds()
        feeds = f.data(**{'url_to_parse': rss.url})

        for entry in feeds.entries:

            if hasattr(entry, 'published_parsed'):
                published = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.published_parsed))
            elif hasattr(entry, 'created_parsed'):
                published = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.created_parsed))
            elif hasattr(entry, 'updated_parsed'):
                published = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.updated_parsed))

            if published == '':
                published = now
            else:
                published = arrow.get(str(published)).to(settings.TIME_ZONE)

            date_triggered = arrow.get(
                str(date_triggered)).to(settings.TIME_ZONE)

            if date_triggered is not None and\
               published is not None and\
               now >= published >= date_triggered:
                my_feeds.append(entry)

        cache.set(consumer + '_' + str(trigger_id), my_feeds)
        cache.set(consumer + '_TOKEN_' + str(trigger_id), consumer_token)
        cache.set('th_rss_uuid_{}'.format(rss.uuid), my_feeds)
        # return the data
        return my_feeds

