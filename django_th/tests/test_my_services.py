# coding: utf-8
from django.test import TestCase


class MyServiceTest(TestCase):

    def setUp(self):
        self.package = "th_rss"
        self.module_name = 'my_rss'
        self.service_name = 'ServiceRss'
        self.full_name = "th_rss.my_rss.ServiceRss"

    def test_full_name(self):
        service_name = self.package.split('_')[1]
        full_name = ''.join((self.package,
                             ".my_",
                             service_name,
                             ".Service",
                             service_name.title()))
        self.assertEqual(self.full_name, full_name)

    def test_module_name(self):
        module_name = "".join(("my_", self.package.split('_')[1]))
        self.assertEqual(self.module_name, module_name)

    def test_service_name(self):
        service_name = "".join(("Service", self.package.split('_')[1].title()))
        self.assertEqual(self.service_name, service_name)
