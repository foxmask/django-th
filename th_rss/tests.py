# coding: utf-8
from django.conf import settings
from th_rss.models import Rss
from th_rss.forms import RssProviderForm
from django_th.tests.test_main import MainTest
import uuid


class RssTest(MainTest):

    """
        RssTest Model
    """
    def create_rss(self):
        trigger = self.create_triggerservice(consumer_name='ServiceRss')
        name = 'Foobar RSS'
        url = 'http://foobar.com/somewhere/in/the/rainbow.rss'
        status = True
        return Rss.objects.create(uuid=uuid.uuid4(),
                                  url=url,
                                  name=name,
                                  trigger=trigger,
                                  status=status)

    def test_rss(self):
        r = self.create_rss()
        self.assertTrue(isinstance(r, Rss))
        self.assertEqual(r.show(), "Services RSS {} {}".format(r.url, r.trigger))

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        r = self.create_rss()
        data = {'name': r.name, 'url': r.url}
        form = RssProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = RssProviderForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th_cache(self):
        self.assertIn('th_rss', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_rss.my_rss.ServiceRss',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)
