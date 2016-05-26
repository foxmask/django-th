# coding: utf-8
from django.conf import settings
from django_th.models import TriggerService, UserService, ServicesActivated
from django_th.tests.test_main import MainTest
from th_pelican.models import Pelican
from th_pelican.forms import PelicanProviderForm, PelicanConsumerForm
from th_pelican.my_pelican import ServicePelican


class PelicanTest(MainTest):

    """
        pelicanTest Model
    """

    def create_triggerservice(self,
                              date_created="20130610",
                              description="My first Service",
                              status=True,
                              consumer_name="ServicePelican"):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name=consumer_name, status=True,
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
                                      title='My Pelican',
                                      url='http://localhost.com',
                                      path='/tmp/',
                                      name=name,
                                      category='News',
                                      status=status)

    def test_pelican(self):
        """
           Test if the creation of the pelican object looks fine
        """
        d = self.create_pelican()
        self.assertTrue(isinstance(d, Pelican))
        self.assertEqual(d.show(), "My Pelican {}".format(d.name))
        self.assertEqual(d.__str__(), d.name)

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

    def test_save_data(self):
        pelican = self.create_pelican()
        token = 'AZERTY1234'
        data = {'title': 'my title', 'category': 'News', 'tags': 'Python'}

        s = ServicePelican()
        r = s.save_data(token, pelican.trigger_id, **data)
        self.assertTrue(r, True)

        pelican.path = '/tmp/foo'
        pelican.save()
        s = ServicePelican()
        r = s.save_data(token, pelican.trigger_id, **data)
        self.assertFalse(r, False)
