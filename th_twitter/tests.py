# coding: utf-8
from django.conf import settings
from th_twitter.models import Twitter
from th_twitter.forms import TwitterProviderForm, TwitterConsumerForm
from django_th.tests.test_main import MainTest


class TwitterTest(MainTest):

    """
        TwitterTest Model
    """

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_TWITTER)
        self.assertIn('consumer_key', settings.TH_TWITTER)
        self.assertIn('consumer_secret', settings.TH_TWITTER)

    def test_get_config_th_cache(self):
        self.assertIn('th_twitter', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_twitter.my_twitter.ServiceTwitter',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

    def create_twitter(self):
        trigger = self.create_triggerservice(consumer_name='ServiceTwitter')
        tag = 'twitter'
        screen = '@johndoe'
        status = True
        return Twitter.objects.create(tag=tag, screen=screen,
                                      trigger=trigger, status=status)

    def test_twitter(self):
        t = self.create_twitter()
        self.assertTrue(isinstance(t, Twitter))
        self.assertEqual(t.show(), "My Twitter %s %s" % (t.screen, t.tag))
        self.assertEqual(t.__str__(), "{}".format(t.screen))

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        t = self.create_twitter()
        data = {'screen': t.screen, 'tag': t.tag}
        form = TwitterProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = TwitterProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        t = self.create_twitter()
        data = {'screen': t.screen, 'tag': t.tag}
        form = TwitterConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        form = TwitterConsumerForm(data={})
        self.assertFalse(form.is_valid())
