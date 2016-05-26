# coding: utf-8
from django.conf import settings
from th_rss.models import Rss
from th_rss.forms import RssProviderForm
from django_th.tests.test_main import MainTest
import uuid
import arrow


class RssTest(MainTest):

    """
        RssTest Model
    """

    def create_rss(self):
        trigger = self.create_triggerservice(consumer_name='ServiceRss')
        name = 'TriggerHappy RSS'
        url = 'https://blog.trigger-happy.eu/feeds/all.rss.xml'
        status = True
        return Rss.objects.create(uuid=uuid.uuid4(),
                                  url=url,
                                  name=name,
                                  trigger=trigger,
                                  status=status)

    def test_rss(self):
        r = self.create_rss()
        self.assertTrue(isinstance(r, Rss))
        self.assertEqual(
            r.show(), "Services RSS {} {}".format(r.url, r.trigger))
        self.assertEqual(r.__str__(), r.url)

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

    def test_read_data(self):
        r = self.create_rss()
        from th_rss.my_rss import ServiceRss
        date_triggered = arrow.get('2013-05-11T21:23:58.970460+00:00')
        kwargs = {'date_triggered': date_triggered,
                  'trigger_id': r.trigger_id,
                  'model_name': 'Rss'}
        self.assertTrue('date_triggered' in kwargs)
        self.assertTrue('trigger_id' in kwargs)
        self.assertTrue('model_name' in kwargs)
        self.assertEqual(kwargs['model_name'], 'Rss')

        s = ServiceRss()
        data = s.read_data(**kwargs)

        self.assertTrue(type(data) is list)

    def test_process_data(self):
        r = self.create_rss()
        from th_rss.my_rss import ServiceRss
        kwargs = {'trigger_id': r.trigger_id}

        self.assertTrue('trigger_id' in kwargs)

        kw = {'cache_stack': 'th_rss',
              'trigger_id': str(kwargs['trigger_id'])}

        self.assertTrue('cache_stack' in kw)
        self.assertTrue('trigger_id' in kw)

        s = ServiceRss()
        data = s.process_data(**kw)
        if data:
            self.assertTrue(type(data) is list)
