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

cache = caches['th_rss']


class ServiceRss(ServicesMgr):
    """
        Service RSS
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceRss, self).__init__(token, **kwargs)

    def _get_published(self, entry):
        """
        get the 'published' attribute
        :param entry:
        :return:
        """
        published = ''
        if hasattr(entry, 'published_parsed'):
            if entry.published_parsed is not None:
                published = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.published_parsed))
        elif hasattr(entry, 'created_parsed'):
            if entry.created_parsed is not None:
                published = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.created_parsed))
        elif hasattr(entry, 'updated_parsed'):
            if entry.updated_parsed is not None:
                published = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.updated_parsed))
        return published

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id and model name
            :type kwargs: dict
            :rtype: dict
        """
        date_triggered = kwargs.get('date_triggered')
        trigger_id = kwargs.get('trigger_id')
        kwargs['model_name'] = 'Rss'

        # get the URL from the trigger id
        rss = super(ServiceRss, self).read_data(**kwargs)

        logger.debug("RSS Feeds from %s : url %s", rss.name, rss.url)

        now = arrow.utcnow().to(settings.TIME_ZONE)
        my_feeds = []

        # retrieve the data
        feeds = Feeds(**{'url_to_parse': rss.url}).datas()

        for entry in feeds.entries:
            # entry.*_parsed may be None when the date in a RSS Feed is invalid
            # so will have the "now" date as default
            published = self._get_published(entry)

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

        cache.set('th_rss_' + str(trigger_id), my_feeds)
        cache.set('th_rss_uuid_{}'.format(rss.uuid), my_feeds)
        # return the data
        return my_feeds
