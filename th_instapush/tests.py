# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User

from django_th.models import TriggerService, UserService, ServicesActivated
from th_instapush.models import Instapush
from th_instapush.forms import InstapushConsumerForm


class InstapushTest(TestCase):

    """
        InstapushTest Model
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
            name='ServiceInstapush', status=True,
            auth_required=True, description='Service Instapush')
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

    def create_instapush(self):
        """
            Create a Instapush object related to the trigger object
        """
        trigger = self.create_triggerservice()
        event_name = 'signups'
        tracker_name = 'email'
        status = True
        return Instapush.objects.create(trigger=trigger,
                                        app_id='1234',
                                        app_secret='k33p1ts3cr3t',
                                        event_name=event_name,
                                        tracker_name=tracker_name,
                                        status=status)

    def test_instapush(self):
        """
           Test if the creation of the Instapush object looks fine
        """
        d = self.create_instapush()
        self.assertTrue(isinstance(d, Instapush))
        self.assertEqual(d.show(), "My Instapush %s" % d.name)

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_instapush()
        data = {'event_name': d.event_name, 'tracker_name': d.tracker_name,
                'app_id': d.app_id, 'app_secret': d.app_secret}
        form = InstapushConsumerForm(data=data)
        self.assertTrue(form.is_valid())
