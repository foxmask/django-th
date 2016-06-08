# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_todoist.models import Todoist
from django_th.models import TriggerService, UserService, ServicesActivated
from th_todoist.forms import TodoistProviderForm, TodoistConsumerForm


class TodoistTest(TestCase):

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
