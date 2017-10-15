# coding: utf-8
from django.conf import settings

from django_th.tests.test_main import MainTest
from th_pushbullet.models import Pushbullet
from th_pushbullet.forms import PushbulletProviderForm, PushbulletConsumerForm


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
        return Pushbullet.objects.create(trigger=trigger, type=type,
                                         status=status)

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
