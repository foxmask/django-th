# coding: utf-8
from unittest.mock import patch

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from django_th.models import TriggerService, UserService, ServicesActivated
from th_wallabag.models import Wallabag
from th_wallabag.forms import WallabagProviderForm, WallabagConsumerForm
from th_wallabag.my_wallabag import ServiceWallabag


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
        self.token = 'AZERTY'
        self.trigger_id = 1
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else'}

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
        self.trigger_id = trigger.id
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


class ServiceWallabagTest(WallabagTest):

    def test_read_data(self):
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': 1,
                       'model_name': 'Wallabag'})

        kwargs['model_name'] = 'Wallabag'

        token = 'AZERTY'

        with patch.object(ServiceWallabag, 'read_data') as mock_read_data:
            se = ServiceWallabag(token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with(**kwargs)

    def test_save_data(self):
        kwargs = dict({})
        with patch.object(ServiceWallabag, 'save_data') as mock_save_data:
            se = ServiceWallabag(self.token)
            se.save_data(self.trigger_id, **kwargs)
        mock_save_data.assert_called_once_with(self.trigger_id, **kwargs)
