# coding: utf-8
from django.conf import settings

from django_th.tests.test_main import MainTest
from th_pelican.models import Pelican
from th_pelican.forms import PelicanProviderForm, PelicanConsumerForm
from th_pelican.my_pelican import ServicePelican


class PelicanTest(MainTest):

    """
        pelicanTest Model
    """
    def create_pelican(self):
        """
            Create a Pelican object related to the trigger object
        """
        trigger = self.create_triggerservice(consumer_name='ServicePelican')
        name = 'pelican'
        status = True
        return Pelican.objects.create(trigger=trigger,
                                      title='My Pelican',
                                      url='http://localhost.com',
                                      path='/tmp/',
                                      name=name,
                                      category='News',
                                      tags='foo, bar',
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
        data = {'title': 'my title', 'category': 'News',
                'tags': 'web',
                'my_date': '2016-08-20 13:23:58+00:00'}

        s = ServicePelican()
        r = s.save_data(pelican.trigger_id, **data)
        self.assertTrue(r, True)

        pelican.path = '/tmp/foo'
        pelican.save()
        s = ServicePelican()
        r = s.save_data(pelican.trigger_id, **data)
        self.assertFalse(r, False)
