# coding: utf-8
from unittest.mock import patch, MagicMock
import datetime
from pocket import Pocket

from django.test import TestCase
from django.conf import settings
from th_pocket.models import Pocket as PocketModel
from th_pocket.forms import PocketProviderForm, PocketConsumerForm
from th_pocket.my_pocket import ServicePocket
from django_th.tests.test_main import MainTest


class PocketTest(MainTest):

    """
        PocketTest Model
    """

    def create_pocket(self):
        trigger = self.create_triggerservice(consumer_name='ServicePocket')
        tag = 'test'
        url = 'http://foobar.com/somewhere/in/the/rainbow'
        title = 'foobar'
        tweet_id = ''
        status = True
        return PocketModel.objects.create(tag=tag, url=url, title=title,
                                          tweet_id=tweet_id, trigger=trigger,
                                          status=status)

    def test_pocket(self):
        p = self.create_pocket()
        self.assertTrue(isinstance(p, PocketModel))
        self.assertEqual(p.show(), "My Pocket {}".format(p.url))
        self.assertEqual(p.__str__(), "{}".format(p.url))

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_POCKET)

    def test_get_config_th_cache(self):
        self.assertIn('th_pocket', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_pocket.my_pocket.ServicePocket',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

    """
        Form
    """

    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        p = self.create_pocket()
        data = {'tag': p.tag}
        form = PocketProviderForm(data=data)
        self.assertTrue(form.is_valid())
        form = PocketProviderForm(data={})
        self.assertTrue(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        p = self.create_pocket()
        data = {'tag': p.tag}
        form = PocketConsumerForm(data=data)
        self.assertTrue(form.is_valid())
        form = PocketConsumerForm(data={})
        self.assertTrue(form.is_valid())


class ServicePocketTest(TestCase):
    """
       ServicePocketTest
    """

    def setUp(self):
        self.date_triggered = datetime.datetime(2013, 6, 10, 00, 00)
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else'}
        self.token = 'AZERTY123'
        self.trigger_id = 1
        self.service = ServicePocket(self.token)

    def test_read_data(self):
        kwargs = {'date_triggered': self.date_triggered,
                  'link': 'http://foo.bar/some/thing/else/what/else',
                  'title': 'what else'}
        since = datetime.datetime(2014, 6, 10, 00, 00)
        with patch.object(ServicePocket, 'read_data', return_value={}) as\
                mock_read:
            sp = ServicePocket(self.token)
            data = sp.read_data(**kwargs)
            with patch.object(Pocket, 'get', return_value={}) as mock_method:
                p = Pocket("fake consumer key", self.token)
                p.get(since=since, state="unread")
            mock_method.assert_called_once_with(since=since, state='unread')
        mock_read.assert_called_once_with(**kwargs)

        return data

    def test_save_data(self):

        self.assertTrue(self.token)
        self.assertTrue(isinstance(self.trigger_id, int))
        self.assertIn('link', self.data)
        self.assertIn('title', self.data)
        self.assertIsNotNone(self.data['link'])
        self.assertNotEqual(self.data['title'], '')

        self.service.save_data = MagicMock(name='save_data')
        the_return = self.service.save_data(self.trigger_id, **self.data)

        self.assertTrue(the_return)

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_POCKET)
        self.assertIn('consumer_key', settings.TH_POCKET)

    def test_get_config_th_cache(self):
        self.assertIn('th_pocket', settings.CACHES)

    def test_auth(self):
        pass

    def test_callback(self):
        pass
