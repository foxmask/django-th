# coding: utf-8
import unittest
from django.conf import settings


class TriggerSettingsTestCase(unittest.TestCase):

    """
      check that all the needed config is present
    """

    def test_get_config_service(self):
        self.assertTrue(settings.TH_SERVICES)

    def test_get_config_th(self):
        self.assertTrue(settings.DJANGO_TH)
        self.assertIn('paginate_by', settings.DJANGO_TH)
        self.assertIn('publishing_limit', settings.DJANGO_TH)
        self.assertIn('services_wo_cache', settings.DJANGO_TH)
        self.assertIn('failed_tries', settings.DJANGO_TH)
        self.assertIn('digest_event', settings.DJANGO_TH)
        self.assertIs(type(settings.DJANGO_TH.get('paginate_by')), int)
        self.assertIs(type(settings.DJANGO_TH.get('publishing_limit')), int)
        self.assertIs(type(settings.DJANGO_TH.get('processes')), int)
        self.assertIs(type(settings.DJANGO_TH.get('services_wo_cache')), list)
        self.assertIs(type(settings.DJANGO_TH.get('failed_tries')), int)
        self.assertIs(type(settings.DJANGO_TH.get('digest_event')), bool)
        self.assertIs(type(settings.DJANGO_TH.get('sharing_media')), bool)
        self.assertIn('django_th', settings.CACHES)

    def test_get_services_list(self):
        th_service = (
            'th_rss.my_rss.ServiceRss',
            # 'th_pocket.my_pocket.ServicePocket',
            # 'th_evernote.my_evernote.ServiceEvernote',
            # 'th_twitter.my_twitter.ServiceTwitter',
            # 'th_trello.my_trello.ServiceTrello',
        )
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)
