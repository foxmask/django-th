# coding: utf-8
import datetime
import time

from django.test import TestCase
from django.conf import settings
from th_pocket.models import Pocket
from th_pocket.forms import PocketProviderForm, PocketConsumerForm
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
        return Pocket.objects.create(tag=tag, url=url, title=title,
                                     tweet_id=tweet_id, trigger=trigger,
                                     status=status)

    def test_pocket(self):
        p = self.create_pocket()
        self.assertTrue(isinstance(p, Pocket))
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


try:
    from unittest import mock
except ImportError:
    import mock


class ServicePocketTest(TestCase):
    """
       ServicePocketTest
    """

    def setUp(self):
        self.date_triggered = datetime.datetime(2013, 6, 10, 00, 00)
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else'}

    def test_process_data(self, token='AZERTY123', trigger_id=1):
        since = int(
            time.mktime(datetime.datetime.timetuple(self.date_triggered)))

        datas = list()
        self.assertTrue(isinstance(self.date_triggered, datetime.datetime))
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertTrue(isinstance(since, int))
        self.assertTrue(isinstance(datas, list))

        pocket_instance = mock.Mock()
        pocket_instance.method(since=since, state="unread")
        pocket_instance.method.assert_called_with(since=since, state="unread")

        return datas

    def test_save_data(self, token='AZERTY123', trigger_id=1):

        the_return = False
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('link', self.data)
        self.assertIn('title', self.data)
        self.assertIsNotNone(self.data['link'])
        self.assertNotEqual(self.data['title'], '')

        # from th_pocket.models import Pocket as PocketModel
        # trigger = PocketModel.objects.get(trigger_id=trigger_id)
        # tags = trigger.tag.lower()
        tags = ('test',)

        title = (self.data['title'] if 'title' in self.data else '')

        pocket_instance = mock.Mock(return_value=True)
        pocket_instance.method(url=self.data['link'], title=title, tags=tags)
        pocket_instance.method.assert_called_with(url=self.data['link'],
                                                  title=title, tags=tags)

        if pocket_instance():
            the_return = True

        return the_return

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
