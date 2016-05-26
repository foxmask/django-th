# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_wallabag.models import Wallabag
from django_th.models import TriggerService, UserService, ServicesActivated
from th_wallabag.forms import WallabagProviderForm, WallabagConsumerForm


class WallabagTest(TestCase):

    """
        wallabagTest Model
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
            name='ServiceWallabag', status=True,
            auth_required=True, description='Service Wallabag')
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

    def create_wallabag(self):
        """
            Create a Wallabag object related to the trigger object
        """
        trigger = self.create_triggerservice()
        url = 'http://trigger-happy.eu'
        title = 'Trigger Happy'
        status = True
        return Wallabag.objects.create(trigger=trigger,
                                       url=url,
                                       title=title,
                                       status=status)

    def test_wallabag(self):
        """
           Test if the creation of the wallabag object looks fine
        """
        d = self.create_wallabag()
        self.assertTrue(isinstance(d, Wallabag))
        self.assertEqual(d.show(), "My Wallabag %s" % d.url)

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_wallabag()
        data = {'url': d.url}
        form = WallabagProviderForm(data=data)
        self.assertTrue(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_wallabag()
        data = {'url': d.url}
        form = WallabagConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th_cache(self):
        self.assertIn('th_wallabag', settings.CACHES)
