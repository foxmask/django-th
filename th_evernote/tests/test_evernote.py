# coding: utf-8
import datetime
import time

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_evernote.models import Evernote
from django_th.models import TriggerService, UserService, ServicesActivated
from th_evernote.forms import EvernoteProviderForm, EvernoteConsumerForm


class EvernoteTest(TestCase):

    """
        EvernoteTest Model
    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        user = self.user
        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceEvernote', status=True,
            auth_required=True, description='Service Evernote')
        provider = UserService.objects.create(user=user,
                                              token="",
                                              name=service_provider)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_consumer)
        return TriggerService.objects.create(provider=provider,
                                             consumer=consumer,
                                             user=user,
                                             date_created=date_created,
                                             description=description,
                                             status=status)

    def create_evernote(self):
        trigger = self.create_triggerservice()
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
        self.assertEqual(ev.show(), "My Evernote %s" % ev.title)

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

    def test_process_data(self, token='AZERTY123',
                          trigger_id=1, date_triggered=''):
        token = self.token
        date_triggered = self.date_triggered
        trigger_id = self.trigger_id

        since = int(
            time.mktime(datetime.datetime.timetuple(date_triggered)))

        datas = list()
        self.assertTrue(isinstance(self.date_triggered, datetime.datetime))
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertTrue(isinstance(since, int))
        self.assertTrue(isinstance(datas, list))

        self.assertIn('sandbox', settings.TH_EVERNOTE)
        sandbox = settings.TH_EVERNOTE['sandbox']

        client = mock.Mock()
        client.method(token=token, sandbox=sandbox)
        client.method.assert_called_with(token=token, sandbox=sandbox)

        return datas

    def test_save_data(self, token='AZERTY123', trigger_id=1):
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

    def test_get_evernote_client(self, token=None):
        """
            get the token from evernote
        """

        self.assertIn('sandbox', settings.TH_EVERNOTE)
        sandbox = settings.TH_EVERNOTE['sandbox']
        client = mock.Mock(return_value=True)
        client.method(token=token, sandbox=sandbox)
        client.method.assert_called_with(token=token, sandbox=sandbox)

        self.assertIn('consumer_key', settings.TH_EVERNOTE)
        self.assertIn('consumer_secret', settings.TH_EVERNOTE)
        self.assertIn('sandbox', settings.TH_EVERNOTE)
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

    def auth(self):
        pass

    def callback(self):
        pass
