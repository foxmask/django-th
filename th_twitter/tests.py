# coding: utf-8
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.core.cache import caches

from th_twitter.models import Twitter
from th_twitter.forms import TwitterProviderForm, TwitterConsumerForm
from th_twitter.my_twitter import ServiceTwitter
from django_th.tests.test_main import MainTest

cache = caches['th_twitter']


class TwitterTest(MainTest):

    """
        TwitterTest Model
    """

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_TWITTER)
        self.assertIn('consumer_key', settings.TH_TWITTER)
        self.assertIn('consumer_secret', settings.TH_TWITTER)

    def test_get_config_th_cache(self):
        self.assertIn('th_twitter', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_twitter.my_twitter.ServiceTwitter',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

    def create_twitter(self):
        trigger = self.create_triggerservice(consumer_name='ServiceTwitter')
        tag = 'twitter'
        screen = '@johndoe'
        status = True
        return Twitter.objects.create(tag=tag, screen=screen,
                                      trigger=trigger, status=status)

    def test_twitter(self):
        t = self.create_twitter()
        self.assertTrue(isinstance(t, Twitter))
        self.assertEqual(t.show(), "My Twitter %s %s" % (t.screen, t.tag))
        self.assertEqual(t.__str__(), "{}".format(t.screen))

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        t = self.create_twitter()
        data = {'screen': t.screen, 'tag': t.tag}
        form = TwitterProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = TwitterProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        t = self.create_twitter()
        data = {'screen': t.screen, 'tag': t.tag}
        form = TwitterConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        form = TwitterConsumerForm(data={})
        self.assertFalse(form.is_valid())


class ServiceTwitterTest(TwitterTest):
    """
       ServiceTwitterTest
    """

    def setUp(self):
        super(ServiceTwitterTest, self).setUp()
        self.data = {'text': 'something #thatworks'}
        self.token = 'QWERTY123#TH#12345'
        self.trigger_id = 1
        self.service = ServiceTwitter(self.token)

    def test_read_data(self):
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'model_name': 'Twitter'})

        # date_triggered = kwargs.get('date_triggered')
        trigger_id = kwargs.get('trigger_id')

        kwargs['model_name'] = 'Twitter'

        # filter_string = se.set_twitter_filter(date_triggered, self.ev)
        # twitter_filter = se.set_note_filter(filter_string)
        data = []
        cache.set('th_twitter_' + str(trigger_id), data)

        with patch.object(ServiceTwitter, 'read_data') as mock_read_data:
            se = ServiceTwitter(self.token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with(**kwargs)

    def test_save_data(self):
        token = self.token
        trigger_id = self.trigger_id

        the_return = False
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('text', self.data)
        self.assertNotEqual(self.data['text'], '')

        self.service.save_data = MagicMock(name='save_data')
        the_return = self.service.save_data(trigger_id, **self.data)

        self.assertTrue(the_return)
