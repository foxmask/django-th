# -*- coding: utf-8 -*-
import feedparser

__all__ = ['Feeds']


class Feeds(object):

    URL_TO_PARSE = ''
    USER_AGENT = 'TriggerHappy/1.0 +http://trigger-happy.eu/'

    def data(self, **kwargs):
        """
            read the data from a given URL or path to a local file
            :param kwargs:
            :return:
        """
        try:
            assert 'url_to_parse' in kwargs
            assert kwargs['url_to_parse'] != ''
            self.URL_TO_PARSE = kwargs['url_to_parse']
            return feedparser.parse(self.URL_TO_PARSE, agent=self.USER_AGENT)
        except AssertionError as e:
            print(e)
            return False

