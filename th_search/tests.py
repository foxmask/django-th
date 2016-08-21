from django.test import TestCase
from django.conf import settings


class SearchTest(TestCase):

    def test_get_config(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.HAYSTACK_CONNECTIONS)
