# -*- coding: utf-8 -*-
import feedparser

__all__ = ['Feeds']


class Feeds(object):

    URL_TO_PARSE = ''

    def __init__(self, **kwargs):
        if 'url_to_parse' in kwargs:
            self.URL_TO_PARSE = kwargs['url_to_parse']
        else:
            print 'Missing argument url_to_parse'

    @property
    def datas(self):
        url_to_parse = self.URL_TO_PARSE

        datas = feedparser.parse(url_to_parse)
        for entry in datas.entries:
            print entry
            yield entry
