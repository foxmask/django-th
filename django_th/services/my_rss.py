# -*- coding: utf-8 -*-

from .services import ServicesMgr
from django_th.lib.feedsservice import Feeds


class ServiceRss(ServicesMgr):

    def get_title(self):
        self.title = self.data['title']

    def get_body(self):
        self.body = self.data['description']

    def process_data(self, obj_id):
        # call the model
        from django_th.models.rss import ServiceRss
        # call the cache
        from django.core.cache import get_cache

        # get the URL from the trigger id
        rss = ServiceRss.objects.get(id=obj_id)
        self.rss_name = rss.name

        # get the cache settings
        parms = self._cache_settings()
        # cache rss backend + parms
        cache = get_cache('rss', **parms)
        # datas from the cache
        self.data = cache.get(self.rss_name)
        # data not in cache or expiried
        if self.data is None:
            # retreive the data
            feeds = Feeds(**{'url_to_parse': rss.url}).datas()
            # put in cache
            cache.set(self.rss_name, feeds, parms['rss']['TIMEOUT'])
            # get the cache
            self.data = cache.get(self.rss_name)
        # return the datas
        return self.data

    def _cache_settings(self):
        from django.conf import settings
        location = settings.CACHES['rss']['LOCATION'] + '/' + self.rss_name
        timeout = settings.CACHES['rss']['TIMEOUT']
        parms = {'rss': {'LOCATION': location, 'TIMEOUT': timeout}}
        return parms
