# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from th_rss.models import Rss
from django_th.models import TriggerService, UserService, ServicesActivated
from th_rss.forms import RssProviderForm


class RssTest(TestCase):

    """
        RssTest Model
    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        user = self.user
        service_provider = ServicesActivated.objects.create(
            name='ServiceRss', status=True,
            auth_required=False, description='Service Rss')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceEvernote', status=True,
            auth_required=True, description='Service Evernote')
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

    def create_rss(self):
        trigger = self.create_triggerservice()
        name = 'Foobar RSS'
        url = 'http://foobar.com/somewhere/in/the/rainbow.rss'
        status = True
        return Rss.objects.create(url=url,
                                  name=name,
                                  trigger=trigger,
                                  status=status)

    def test_rss(self):
        r = self.create_rss()
        self.assertTrue(isinstance(r, Rss))
        self.assertEqual(r.show(), "Services RSS %s %s" % (r.url, r.trigger))

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        r = self.create_rss()
        data = {'name': r.name, 'url': r.url}
        form = RssProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = RssProviderForm(data={})
        self.assertFalse(form.is_valid())
