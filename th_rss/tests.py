# coding: utf-8
import arrow

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import RequestFactory

from django_th.tests.test_main import MainTest, setup_view
import django_th

from th_rss.forms import RssProviderForm
from th_rss.models import Rss
from th_rss.views import MyRssFeed, MyRssFeeds

import uuid


class RssTest(MainTest):

    def create_rss(self):
        trigger = self.create_triggerservice(consumer_name='ServiceRss',
                                             provider_name='ServiceEvernote')
        name = 'TriggerHappy RSS'
        url = 'https://blog.trigger-happy.eu/feeds/all.rss.xml'
        status = True
        self.uuid = uuid.uuid4()
        return Rss.objects.create(uuid=self.uuid,
                                  url=url,
                                  name=name,
                                  trigger=trigger,
                                  status=status)


class RssModelTest(RssTest):
    """
        RssModelTest Model
    """

    def test_rss(self):
        r = self.create_rss()
        self.assertTrue(isinstance(r, Rss))
        self.assertEqual(
            r.show(),
            "Services RSS %s %s" % (r.url, r.trigger)
        )
        self.assertEqual(r.__str__(), r.url)


class RssFormTest(RssTest):
    """
        RssFormTest
    """

    def test_valid_provider_form(self):
        r = self.create_rss()
        data = {'name': r.name, 'url': r.url}
        form = RssProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = RssProviderForm(data={})
        self.assertFalse(form.is_valid())

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


class TestMyRssFeed(RssTest):

    def setUp(self):
        super(TestMyRssFeed, self).setUp()
        self.create_rss()
        self.template = 'rss/my_feed.html'
        self.request = RequestFactory().get('/th/myfeeds/{}'.format(self.uuid))

    def test_get(self):
        view = MyRssFeed.as_view(template_name=self.template)
        response = view(self.request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], self.template)
        self.assertEqual(response.context_data['lang'], settings.LANGUAGE_CODE)
        self.assertEqual(response.context_data['version'],
                         django_th.__version__)

    def test_context_data(self):
        kwargs = {'uuid': self.uuid}

        view = MyRssFeed(template_name=self.template)
        view = setup_view(view, self.request)

        context = view.get_context_data(**kwargs)
        context['lang'] = settings.LANGUAGE_CODE
        context['version'] = django_th.__version__
        context['uuid'] = self.uuid

        self.assertTrue('lang' in context)
        self.assertTrue('version' in context)
        self.assertTrue('uuid' in context)


class MyRssFeedsListViewTestCase(MainTest):

    def setUp(self):
        super(MyRssFeedsListViewTestCase, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get(self):
        template_name = "rss/my_feeds.html"
        # Setup request and view.
        request = RequestFactory().get(reverse('my_feeds'))
        request.user = self.user
        view = MyRssFeeds.as_view(template_name=template_name)
        # Run.
        response = view(request, user=request.user)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], template_name)
