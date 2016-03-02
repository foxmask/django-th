# coding: utf-8
import datetime
import time

from django.test import TestCase
from django.conf import settings
from th_readability.models import Readability
from django_th.tests.test_main import MainTest


class ReadabilityTest(MainTest):

    """
        ReadabilityTest Model
    """
    def create_readability(self):
        trigger = self.create_triggerservice(
            consumer_name='ServiceReadability')
        name = 'test'
        tag = 'test tag'
        status = True
        return Readability.objects.create(name=name,
                                          tag=tag,
                                          trigger=trigger,
                                          status=status)

    def test_readability(self):
        r = self.create_readability()
        self.assertTrue(isinstance(r, Readability))
        self.assertEqual(r.show(), "My Readability {}".format(r.name))

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_READABILITY)

    def test_get_config_th_cache(self):
        self.assertIn('th_readability', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_readability.my_readability.ServiceReadability',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)


try:
    from unittest import mock
except ImportError:
    import mock


class ServiceReadabilityTest(TestCase):
    """
       ServiceReadabilityTest
    """
    def setUp(self):
        self.date_triggered = datetime.datetime(2013, 6, 10, 00, 00)
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else'}
        self.consumer_key = settings.TH_READABILITY['consumer_key']
        self.consumer_secret = settings.TH_READABILITY['consumer_secret']

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_READABILITY)
        self.assertIn('consumer_key', settings.TH_READABILITY)
        self.assertIn('consumer_secret', settings.TH_READABILITY)

    def test_get_config_th_cache(self):
        self.assertIn('th_readability', settings.CACHES)

    def test_process_data(self, token='AZERTY123#TH#AZERTY123', trigger_id=1):
        since = int(
            time.mktime(datetime.datetime.timetuple(self.date_triggered)))
        self.assertIn('#TH#', token)
        token_key, token_secret = token.split('#TH#')

        datas = list()
        self.assertTrue(isinstance(self.date_triggered, datetime.datetime))
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertTrue(isinstance(since, int))
        self.assertTrue(isinstance(datas, list))

        client = mock.Mock()
        client.method(consumer_key=self.consumer_key,
                      consumer_secret=self.consumer_secret,
                      token_key=token_key,
                      token_secret=token_secret)
        client.method.assert_called_with(consumer_key=self.consumer_key,
                                         consumer_secret=self.consumer_secret,
                                         token_key=token_key,
                                         token_secret=token_secret)

        return datas

    def test_save_data(self, token='AZERTY123', trigger_id=1):

        the_return = False
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('link', self.data)
        self.assertIn('title', self.data)
        self.assertIsNotNone(self.data['link'])
        self.assertNotEqual(self.data['title'], '')

        tags = ('test',)
        title = (self.data['title'] if 'title' in self.data else '')

        pocket_instance = mock.Mock(return_value=True)
        pocket_instance.method(url=self.data['link'], title=title, tags=tags)
        pocket_instance.method.assert_called_with(url=self.data['link'],
                                                  title=title, tags=tags)

        if pocket_instance():
            the_return = True

        return the_return

    def test_auth(self):
        pass

    def test_callback(self):
        pass
