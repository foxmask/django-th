# coding: utf-8
import datetime
import time

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_readability.models import Readability
from django_th.models import TriggerService, UserService, ServicesActivated


class ReadabilityTest(TestCase):

    """
        ReadabilityTest Model
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
            name='ServiceRss', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceReadability', status=True,
            auth_required=True, description='Service Readability')
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

    def create_readability(self):
        trigger = self.create_triggerservice()
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
        self.assertEqual(r.show(), "My Readability %s" % (r.name))

    """
        Form
    """
    # no need to test if the tag is filled or not as it's not mandatory


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

        #from th_pocket.models import Pocket as PocketModel
        #trigger = PocketModel.objects.get(trigger_id=trigger_id)
        # tags = trigger.tag.lower()
        tags = ('test',)

        title = ''
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
