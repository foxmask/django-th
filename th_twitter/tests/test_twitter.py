# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from th_twitter.models import Twitter
from django_th.models import TriggerService, UserService, ServicesActivated
from th_twitter.forms import TwitterProviderForm, TwitterConsumerForm


class TwitterTest(TestCase):

    """
        TwitterTest Model
    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        user = self.user
        service_provider = ServicesActivated.objects.create(
            name='ServiceTwitter', status=True,
            auth_required=False, description='Service Twitter')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceEvernote', status=True,
            auth_required=True, description='Service Evernote')
        provider = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_provider)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_consumer)
        return TriggerService.objects.create(provider=provider,
                                             consumer=consumer,
                                             user=user,
                                             date_created=date_created,
                                             description=description,
                                             status=status)

    def create_twitter(self):
        trigger = self.create_triggerservice()
        tag = 'twitter'
        screen = '@johndoe'
        status = True
        return Twitter.objects.create(tag=tag, screen=screen, trigger=trigger, status=status)

    def test_twitter(self):
        t = self.create_twitter()
        self.assertTrue(isinstance(t, Twitter))
        self.assertEqual(t.show(), "My Twitter %s %s" % (t.screen, t.tag))

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
