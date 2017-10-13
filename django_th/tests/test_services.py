# coding: utf-8
from django.test import Client

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    pass

from django_th.services.services import ServicesMgr
from django_th.tests.test_main import MainTest


class ServicesMgrTestCase(MainTest):

    def setUp(self):
        super(ServicesMgrTestCase, self).setUp()
        arg = ''
        self.service = ServicesMgr(arg)
        self.service.consumer_key = 'azerty'
        self.service.consumer_secret = 'qsdfghjk'
        self.service.name = 'ServiceRss'

        self.oauth = 'oauth1'
        self.request = Client()

    def test_set_title(self):
        data = {'title': 'foobar'}
        self.assertTrue('title' in data)
        data = {'link': 'http://localhost/url/to/news'}
        self.assertTrue('title' not in data)
        self.assertTrue('link' in data)

    def test_set_content_summary(self):
        data = {'summary_detail': 'some summary'}
        res = self.service.set_content(data)
        self.assertTrue(type(res) is str)

    def test_set_content_description(self):
        data = {'description': 'foobar'}
        res = self.service.set_content(data)
        self.assertTrue(type(res) is str)

    def test_set_content_empty(self):
        data = {'content': ''}
        res = self.service.set_content(data)
        self.assertTrue(type(res) is str)

    def test_set_content(self):
        content = list()
        content.append({'foobar': 'value'})
        data = {'content': content}
        res = self.service.set_content(data)
        self.assertTrue(type(res) is str)

    def test_save_data(self):
        trigger_id = 1
        data = dict({'title': 'a title', 'summary_detail': 'a content'})
        data['output_format'] = 'md'
        title, content = self.service.save_data(trigger_id, **data)
        self.assertTrue(title)
        self.assertTrue(content)

    def test_str(self):
        self.assertEqual(self.service.__str__(), self.service.name)
