# coding: utf-8
from django.test import TestCase

from django.conf import settings
from django_th.my_services import MyService


class MyServiceTest(TestCase):

    def setUp(self):
        self.package = "th_rss"
        self.module_name = 'my_rss'
        self.service_name = 'ServiceRss'
        self.full_name = "th_rss.my_rss.ServiceRss"

    def test_full_name(self):
        service_long = MyService.full_name('th_rss')
        self.assertEqual(self.full_name, service_long)
        self.assertTrue(service_long in settings.TH_SERVICES)

    def test_module_name(self):
        module_name = MyService.module_name('th_rss')
        self.assertEqual(self.module_name, module_name)

    def test_service_name(self):
        service_name = MyService.service_name('th_rss')
        self.assertEqual(self.service_name, service_name)

    def test_all_packages(self):
        all_packages = MyService.all_packages()
        self.assertIsInstance(all_packages, list)
