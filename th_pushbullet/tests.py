# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_pushbullet.models import Pushbullet
from django_th.models import TriggerService, UserService, ServicesActivated
from th_pushbullet.forms import PushbulletProviderForm, PushbulletConsumerForm


class PushbulletTest(TestCase):

    """
        PushbulletTest Model
    """
    def setUp(self):
        """
           create a user
        """
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServicePushbullet', status=True,
            auth_required=True, description='Service Pushbullet')
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

    def create_pushb(self):
        """
            Create a Pushbullet object related to the trigger object
        """
        trigger = self.create_triggerservice()
        type = 'note'
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
        self.assertTrue(settings.TH_PUSHBULLET)
