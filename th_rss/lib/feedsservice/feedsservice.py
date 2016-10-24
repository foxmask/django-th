# -*- coding: utf-8 -*-
import feedparser

__all__ = ['Feeds']


class Feeds(object):

    URL_TO_PARSE = ''
    USER_AGENT = 'TriggerHappy/1.0 +http://trigger-happy.eu/'

    def __init__(self, **kwargs):

        if 'url_to_parse' in kwargs and kwargs['url_to_parse'] != '':
            self.URL_TO_PARSE = kwargs['url_to_parse']
        else:
            raise KeyError('Missing argument "url_to_parse" eg.'
                           ' url_to_parse="/path/to/local/file.rss" or'
                           ' url_to_parse="http://domain.com/file.rss"')

    def datas(self):
        """
            read the data from a given URL or path to a local file
        """
        data = feedparser.parse(self.URL_TO_PARSE, agent=self.USER_AGENT)

        # when chardet says
        # >>> chardet.detect(data)
        # {'confidence': 0.99, 'encoding': 'utf-8'}
        # bozo says sometimes
        # >>> data.bozo_exception
        # CharacterEncodingOverride('document declared as us-ascii, but parsed as utf-8', )  # invalid Feed
        # so I remove this detection :(
        # if data.bozo == 1:
        #     data.entries = ''

        return data
