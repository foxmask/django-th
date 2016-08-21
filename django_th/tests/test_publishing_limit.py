# coding: utf-8
from django.test import TestCase

from django.conf import settings
from django_th.publishing_limit import PublishingLimit


class PublishingLimitTestCase(TestCase):

    def test_settings(self):
        self.assertTrue('publishing_limit' in settings.DJANGO_TH)

    def test_get_data(self):

        cache_stack = "th_rss"
        cache_data = {}
        trigger_id = 1

        services = PublishingLimit.get_data(cache_stack, cache_data, trigger_id)
        self.assertTrue(len(services) == 0)

    def test_get_data2(self):
        cache_stack = "th_rss"
        cache_data = {'th_rss_1': 'foobar'}
        trigger_id = 1

        services = PublishingLimit.get_data(cache_stack, cache_data, trigger_id)
        self.assertTrue(len(services) > 0)

    def test_get_data3(self):
        cache_stack = "th_rss"
        cache_data = []
        cache_data.append({'th_rss_1': 'foobar'})
        cache_data.append({'th_rss_2': 'foobar'})
        cache_data.append({'th_rss_3': 'foobar'})
        cache_data.append({'th_rss_4': 'foobar'})
        cache_data.append({'th_rss_5': 'foobar'})
        cache_data.append({'th_rss_6': 'foobar'})
        trigger_id = 1

        services = PublishingLimit.get_data(cache_stack, cache_data, trigger_id)
        self.assertTrue(len(services) > 0)
