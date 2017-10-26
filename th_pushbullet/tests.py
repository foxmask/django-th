# coding: utf-8
from django.conf import settings

from django_th.tests.test_main import MainTest
from pushbullet import Pushbullet as Pushb
from th_pushbullet.forms import PushbulletProviderForm, PushbulletConsumerForm
from th_pushbullet.models import Pushbullet
from th_pushbullet.my_pushbullet import ServicePushbullet

from unittest.mock import patch


class PushbulletTest(MainTest):

    """
        PushbulletTest Model
    """
    def create_pushb(self, type='note'):
        """
            Create a Pushbullet object related to the trigger object
        """
        trigger = self.create_triggerservice(consumer_name="ServicePushbullet")
        status = True
        return Pushbullet.objects.create(trigger=trigger, type=type, status=status)

    def test_pushbullet(self):
        """
           Test if the creation of the pushbullet object looks fine
        """
        d = self.create_pushb()
        self.assertTrue(isinstance(d, Pushbullet))
        self.assertEqual(d.show(), "My Pushbullet %s" % d.name)
        self.assertEqual(d.__str__(), "%s" % d.name)

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        data = {'type': 'note', 'device': '', 'email': '', 'channel_tag': ''}
        form = PushbulletProviderForm(data=data)
        self.assertTrue(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        data = {'type': 'note', 'device': '', 'email': '', 'channel_tag': ''}
        form = PushbulletConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_PUSHBULLET_KEY)


class ServicePushbulletTest(PushbulletTest):
    """
       ServicePushbulletTest
    """
    def test_init(self):
        with patch.object(Pushb, '__init__') as mock_pushb:
            mock_pushb.return_value = None
            ServicePushbullet(token='AZERTY123')
        mock_pushb.assert_called_once()

    def test_read_data(self):
        pushb_data = self.create_pushb()
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': pushb_data.trigger_id})
        with patch.object(Pushb, '__init__') as mock_pushb1:
            mock_pushb1.return_value = None
            with patch.object(Pushb, 'get_pushes') as mock_pushb2:
                se = ServicePushbullet(token='AZERTY123')
                se.read_data(**kwargs)
            mock_pushb2.assert_called_once()
        mock_pushb1.assert_called_once()

    def test_save_data_no_token(self):
        pushb_data = self.create_pushb()
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'A nice content with a nice '
                           '<a href="http://domain.tld">foobar link</a>',
                'summary_detail': 'summary foobar',
                'description': 'description foobar'}
        se = ServicePushbullet(token=None)
        result = se.save_data(trigger_id=pushb_data.trigger_id, **data)
        self.assertFalse(result)

    def test_save_data_unknown_type(self):
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'A nice content with a nice '
                           '<a href="http://domain.tld">foobar link</a>',
                'summary_detail': 'summary foobar',
                'description': 'description foobar'}
        with patch.object(Pushb, '__init__') as mock_pushb1:
            mock_pushb1.return_value = None
            # push_note case
            pushb_data = self.create_pushb(type='fake')
            se = ServicePushbullet(token='AZERTY123')
            result = se.save_data(trigger_id=pushb_data.trigger_id, **data)
            self.assertFalse(result)
        mock_pushb1.assert_called_once()

    def test_save_data_note(self):
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'A nice content with a nice '
                           '<a href="http://domain.tld">foobar link</a>',
                'summary_detail': 'summary foobar',
                'description': 'description foobar'}
        with patch.object(Pushb, '__init__') as mock_pushb1:
            mock_pushb1.return_value = None
            # push_note case
            pushb_data = self.create_pushb()
            with patch.object(Pushb, 'push_note') as mock_pushb2:
                se = ServicePushbullet(token='AZERTY123')
                se.save_data(trigger_id=pushb_data.trigger_id, **data)
            mock_pushb2.assert_called_once()
        mock_pushb1.assert_called_once()

    def test_save_data_link(self):
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'A nice content with a nice '
                           '<a href="http://domain.tld">foobar link</a>',
                'summary_detail': 'summary foobar',
                'description': 'description foobar'}
        with patch.object(Pushb, '__init__') as mock_pushb1:
            mock_pushb1.return_value = None
            # push_link case
            pushb_data = self.create_pushb(type='link')
            with patch.object(Pushb, 'push_link') as mock_pushb2:
                se = ServicePushbullet(token='AZERTY123')
                se.save_data(trigger_id=pushb_data.trigger_id, **data)
            mock_pushb2.assert_called_once()
        mock_pushb1.assert_called_once()

    def test_auth(self):
        pass

    def test_callback(self):
        pass
