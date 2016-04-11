from django.test import TestCase
from django.conf import settings


class ThSearchTest(TestCase):

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.HAYSTACK_CONNECTIONS)
