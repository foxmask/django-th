from django.test import TestCase
from django.conf import settings

from haystack.forms import EmptySearchQuerySet
from th_search.forms import TriggerHappySearchForm
from th_search.views import TriggerHappySearchView


class ThSearchTest(TestCase):

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.HAYSTACK_CONNECTIONS)


class TriggerHappySearchFormViewTestCase(TestCase):

    def test_no_query_found(self):
        form = TriggerHappySearchForm(initial={})
        self.assertEqual(len(form.no_query_found()), len(EmptySearchQuerySet()))

    def test_queryset(self):
        form = TriggerHappySearchForm(initial={})
        self.assertEqual(len(form.no_query_found()), len(EmptySearchQuerySet()))


class TriggerHappySearchViewTestCase(TestCase):

    def test_get_queryset(self):
        pass
