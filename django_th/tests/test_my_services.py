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
        string = MyService.full_name(self.service_name)
        self.assertEqual(self.full_name, string)

    def test_module_name(self):
        string = MyService.module_name(self.module_name)
        self.assertEqual(self.module_name, string)

    def test_service_name(self):
        string = MyService.service_name(self.package)
        self.assertEqual(self.service_name, string)

    def test_all_packages(self):
        all_packages = MyService.all_packages()
        my_services = list()
        for services in settings.TH_SERVICES:
            package = services.split('.')[2]
            my_services.append(package)
        self.assertEqual(all_packages, my_services)
