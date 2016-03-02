# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_pelican.models import Pelican
from django_th.models import TriggerService, UserService, ServicesActivated
from th_pelican.forms import PelicanProviderForm, PelicanConsumerForm


class PelicanTest(TestCase):

    """
        pelicanTest Model
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
            name='ServicePelican', status=True,
            auth_required=True, description='Service Pelican')
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

    def create_pelican(self):
        """
            Create a Pelican object related to the trigger object
        """
        trigger = self.create_triggerservice()
        name = 'pelican'
        status = True
        return Pelican.objects.create(trigger=trigger,
                                      name=name, status=status)

    def test_pelican(self):
        """
           Test if the creation of the pelican object looks fine
        """
        d = self.create_pelican()
        self.assertTrue(isinstance(d, Pelican))
        self.assertEqual(d.show(), "My Pelican %s" % (d.name))

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_pelican()
        data = {'name': d.name, 'title': 'Foobar WebSite',
                'url': 'http://www.google.com', 'tags': 'tag1, tag2',
                'category': 'internet', 'path': '/home/triggerhappy/pelican'}
        form = PelicanProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        """
           test if that form is not a valid provider one
        """
        form = PelicanProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_pelican()
        data = {'name': d.name, 'title': 'Foobar WebSite',
                'url': 'http://www.google.com', 'tags': 'tag1, tag2',
                'category': 'internet', 'path': '/home/triggerhappy/pelican'}
        form = PelicanConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        """
           test if that form is not a valid consumer one
        """
        form = PelicanConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        self.assertTrue(settings.TH_PELICAN_AUTHOR)

    def test_get_services_list(self):
        th_service = ('th_pelican.my_pelican.ServicePelican',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)
