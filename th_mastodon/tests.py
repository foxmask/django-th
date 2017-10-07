# coding: utf-8
from django.conf import settings
from django.core.cache import caches

from th_mastodon.models import Mastodon
from th_mastodon.forms import MastodonProviderForm, MastodonConsumerForm
from django_th.tests.test_main import MainTest

cache = caches['django_th']


class MastodonTest(MainTest):

    """
        MastodonTest Model
    """

    def test_get_services_list(self):
        th_service = ('th_mastodon.my_mastodon.ServiceMastodon',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

    def create_masto(self, tooter='@foxmask@mamot.fr', timeline='home',
                     tag='millepieds', fav=False):
        trigger = self.create_triggerservice(consumer_name='ServiceMastodon')
        resu = Mastodon.objects.create(tooter=tooter, timeline=timeline,
                                       tag=tag, fav=fav, since_id=1,
                                       max_id=0,
                                       trigger=trigger, status=True)
        return resu

    def test_mastodon(self):
        m = self.create_masto()
        print(m)
        self.assertTrue(isinstance(m, Mastodon))
        self.assertEqual(m.show(), "My Mastodon %s %s" %
                         (m.timeline, m.trigger))
        self.assertEqual(m.__str__(), "{}".format(m.timeline))

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        m = self.create_masto()
        data = {'tooter': m.tooter,
                'timeline': m.timeline,
                'tag': m.tag,
                'fav': m.fav}
        form = MastodonProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = MastodonProviderForm(data={'tooter': '',
                                          'timeline': '',
                                          'tag': '', 'fav': ''})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        m = self.create_masto()
        data = {'tooter': m.tooter,
                'timeline': m.timeline,
                'tag': m.tag,
                'fav': m.fav}
        form = MastodonConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        # when a field is empty the clean() function set it as None
        form = MastodonConsumerForm(data={'tooter': '',
                                          'timeline': '',
                                          'tag': '', 'fav': False})
        self.assertFalse(form.is_valid())
