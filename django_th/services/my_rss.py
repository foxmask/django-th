# -*- coding: utf-8 -*-
# django_th classes
from .services import ServicesMgr
from django_th.lib.feedsservice import Feeds
# django classes
from django.utils.log import getLogger

logger = getLogger('django_th.trigger_happy')


class ServiceRss(ServicesMgr):

    def process_data(self, obj_id):
        # call the model
        from django_th.models.rss import Rss
        # call the cache
        from django.core.cache import get_cache

        # get the URL from the trigger id
        rss = Rss.objects.get(id=obj_id)
        self.name = rss.name

        logger.debug("RSS Feeds from %s : url %s", self.name, rss.url)

        # get the cache settings if any
        parms = self._cache_settings()
        # check if the cache is set otherwise no cache support at all
        if 'rss' in parms:
            # cache rss backend + parms
            cache = get_cache('rss', **parms)
            # datas from the cache
            self.data = cache.get(self.name)
        # data not in cache or expiried
        if self.data is None or len(self.data) == 0:
            # retreive the data
            feeds = Feeds(**{'url_to_parse': rss.url}).datas()
            # put in cache
            if 'rss' in parms:
                cache.set(self.name, feeds, parms['rss']['TIMEOUT'])
                # get the cache
                self.data = cache.get(self.name)
            else:
                self.data = feeds
        # return the datas
        return self.data

    def _cache_settings(self):
        from django.conf import settings
        parms = {}
        if 'rss' in settings.CACHES:
            location = settings.CACHES['rss']['LOCATION'] + '/' + self.name
            timeout = settings.CACHES['rss']['TIMEOUT']
            parms = {'rss': {'LOCATION': location, 'TIMEOUT': timeout}}
        return parms
