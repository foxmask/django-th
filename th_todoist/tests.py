# coding: utf-8
from unittest.mock import patch

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from django_th.models import TriggerService, UserService, ServicesActivated
from th_todoist.models import Todoist
from th_todoist.forms import TodoistProviderForm, TodoistConsumerForm
from th_todoist.my_todoist import ServiceTodoist


class TodoistTest(TestCase):

    def test_get_config_th_cache(self):
        self.assertIn('th_todoist', settings.CACHES)

    """
        TodoistTest Model
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

        self.token = 'AZERTY123'
        self.trigger_id = 1

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
            name='ServiceTodoist', status=True,
            auth_required=True, description='Service Todoist')
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

    def create_todoist(self):
        """
            Create a Todoist object related to the trigger object
        """
        trigger = self.create_triggerservice()
        name = 'todoist'
        status = True
        return Todoist.objects.create(trigger=trigger, name=name, status=status)

    def test_todoist(self):
        """
           Test if the creation of the todoist object looks fine
        """
        d = self.create_todoist()
        self.assertTrue(isinstance(d, Todoist))
        self.assertEqual(d.show(), "My Todoist %s" % d.name)
        self.assertEqual(d.__str__(), "%s" % d.name)

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_todoist()
        data = {'name': d.name}
        form = TodoistProviderForm(data=data)
        self.assertTrue(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_todoist()
        data = {'name': d.name}
        form = TodoistConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_TODOIST)

    def test_read_data(self):
        """
           Test if the creation of the Todoist object looks fine
        """
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'model_name': 'Todoist'})

        with patch.object(ServiceTodoist, 'read_data') as mock_read_data:
            se = ServiceTodoist(self.token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with(**kwargs)

    def test_save_data(self):
        """
           Test if the creation of the Todoist object looks fine
        """
        self.create_todoist()
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'foobar'}

        se = ServiceTodoist(self.token)
        se.save_data(self.trigger_id, **data)
