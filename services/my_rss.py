# -*- coding: utf-8 -*-

from .services import ServicesMgr
from django_th.lib.feedsservice import Feeds


class ServiceRss(ServicesMgr):

    def get_title(self):
        self.title = self.data['title']

    def get_body(self):
        self.body = self.data['description']

    def process_data(self, url):

        feeds = Feeds(**{'url_to_parse': url})
        self.data = feeds.datas()

        return self.data
