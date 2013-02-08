# -*- coding: utf-8 -*-
import feedparser

__all__ = ['Feeds']


class Feeds(object):

	URL_TO_PARSE = ''	

	def __init__(self, **kwargs):
		
		if 'url_to_parse' in kwargs and kwargs['url_to_parse'] != '':
			self.URL_TO_PARSE = kwargs['url_to_parse']	
		else:
			raise Exception ('Missing argument "url_to_parse" eg. url_to_parse=\'/path/to/local/file.rss\' or url_to_parse=\'http://doamin.com/file.rss\'')

	def datas(self):
		'''
			read the data from a given URL or path to a local file
		'''
		datas = feedparser.parse(self.URL_TO_PARSE)
		for entry in datas.entries:
			yield entry
