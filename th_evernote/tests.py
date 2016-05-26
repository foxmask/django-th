# coding: utf-8
import datetime

from django.test import TestCase
from django.conf import settings
from th_evernote.models import Evernote
from th_evernote.forms import EvernoteProviderForm, EvernoteConsumerForm
from django_th.tests.test_main import MainTest


class EvernoteTest(MainTest):

    """
        EvernoteTest Model
    """

    def create_evernote(self):
        trigger = self.create_triggerservice(consumer_name='ServiceEvernote')
        tag = 'test'
        notebook = 'my notebook'
        title = 'a new note'
        status = True
        return Evernote.objects.create(tag=tag, title=title,
                                       notebook=notebook, trigger=trigger,
                                       status=status)

    def test_evernote(self):
        ev = self.create_evernote()
        self.assertTrue(isinstance(ev, Evernote))
        self.assertEqual(ev.show(), "My Evernote {}".format(ev.title))
        self.assertEqual(ev.__str__(), ev.title)

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        ev = self.create_evernote()
        data = {'tag': ev.tag, 'notebook': ev.notebook}
        form = EvernoteProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = EvernoteProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        ev = self.create_evernote()
        data = {'tag': ev.tag, 'notebook': ev.notebook}
        form = EvernoteConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        form = EvernoteConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_EVERNOTE)

    def test_get_services_list(self):
        th_service = ('th_evernote.my_evernote.ServiceEvernote',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

try:
    from unittest import mock
except ImportError:
    import mock


class ServiceEvernoteTest(TestCase):
    """
       ServiceEvernoteTest
    """

    def setUp(self):
        self.date_triggered = datetime.datetime(2013, 6, 10, 00, 00)
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else',
                     'content': 'foobar',
                     'summary_detail': 'summary foobar',
                     'description': 'description foobar'}
        self.token = 'AZERTY123'
        self.trigger_id = 1

    def test_save_data(self):
        token = self.token
        trigger_id = self.trigger_id

        the_return = False
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('content', self.data)
        self.assertIn('summary_detail', self.data)
        self.assertIn('description', self.data)
        self.assertIn('title', self.data)
        self.assertIsNotNone(self.data['link'])
        self.assertNotEqual(self.data['title'], '')

        self.assertIn('sandbox', settings.TH_EVERNOTE)
        sandbox = settings.TH_EVERNOTE['sandbox']

        client = mock.Mock(return_value=True)
        client.method(token=token, sandbox=sandbox)
        client.method.assert_called_with(token=token, sandbox=sandbox)

        if client():
            the_return = True

        return the_return

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_EVERNOTE)
        self.assertIn('consumer_key', settings.TH_EVERNOTE)
        self.assertIn('consumer_secret', settings.TH_EVERNOTE)
        self.assertIn('sandbox', settings.TH_EVERNOTE)

    def test_get_config_th_cache(self):
        self.assertIn('th_evernote', settings.CACHES)

    def test_get_evernote_client(self, token=None):
        """
            get the token from evernote
        """
        sandbox = settings.TH_EVERNOTE['sandbox']
        client = mock.Mock(return_value=True)
        client.method(token=token, sandbox=sandbox)
        client.method.assert_called_with(token=token, sandbox=sandbox)

        sandbox = settings.TH_EVERNOTE['sandbox']
        consumer_key = settings.TH_EVERNOTE['consumer_key']
        consumer_secret = settings.TH_EVERNOTE['consumer_secret']

        client = mock.Mock(return_value=True)
        client.method(consumer_key=consumer_key,
                      consumer_secret=consumer_secret, sandbox=sandbox)
        client.method.assert_called_with(consumer_key=consumer_key,
                                         consumer_secret=consumer_secret,
                                         sandbox=sandbox)

        return client

    def test_auth(self):
        pass

    def test_callback(self):
        pass
