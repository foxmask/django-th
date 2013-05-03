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
        # get the URL from the trigger id
        rss = ServiceRss.objects.get(id=obj_id)
        # give the url to parse to feedsservice
        feeds = Feeds(**{'url_to_parse': rss.url})
        self.data = self.cache_data(rss.name, feeds.datas())

        return self.data

    def cache_data(self, name, datas):
        import os
        import time
        from django.conf import settings
        cache_file = settings.RSS_CACHE_PATH + '/' + name
        try:
            if os.stat(cache_file).s_isreg:
                if os.stat(cache_file).st_ctime > time() + settings.RSS_CACHE_LIFETIME:
                    os.unlink(cache_file, datas)
        except OSError:
            print "file not found, let's create it"
        return self.read_cache(cache_file, datas)

    def read_cache(self, cache_file, datas):
        return datas
