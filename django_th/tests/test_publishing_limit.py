# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django_th.my_services import MyService


class PublishingLimitTestCase(TestCase):

    def test_get_data(self):
        service = "th_rss"

        self.assertTrue(service.startswith('th_'))

        service_long = MyService.full_name(service)

        self.assertTrue(service_long in settings.TH_SERVICES)

        self.assertTrue('publishing_limit' in settings.DJANGO_TH)
