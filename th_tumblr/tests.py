# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django_th.models import TriggerService, UserService, ServicesActivated
from th_tumblr.models import Tumblr
from th_tumblr.my_tumblr import ServiceTumblr
from th_tumblr.forms import TumblrProviderForm, TumblrConsumerForm

from pytumblr import TumblrRestClient
from unittest.mock import patch


class TumblrTest(TestCase):

    """
        tumblrTest Model
    """
    def setUp(self):
        """
           create a user
        """
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceTumblr', status=True,
            auth_required=True, description='Service Tumblr')
        provider = UserService.objects.create(user=user,
                                              token="",
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

    def create_tumblr(self):
        """
            Create a Tumblr object related to the trigger object
        """
        trigger = self.create_triggerservice()
        blogname = 'tumblr'
        tag = ''
        status = True
        return Tumblr.objects.create(trigger=trigger,
                                     blogname=blogname,
                                     tag=tag,
                                     status=status)

    def test_tumblr(self):
        """
           Test if the creation of the tumblr object looks fine
        """
        d = self.create_tumblr()
        self.assertTrue(isinstance(d, Tumblr))
        self.assertEqual(d.show(), "My Tumblr %s" % d.blogname)

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_tumblr()
        data = {'blogname': d.blogname, 'tag': d.tag}
        form = TumblrProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        """
           test if that form is not a valid provider one
        """
        form = TumblrProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_tumblr()
        data = {'blogname': d.blogname, 'tag': d.tag}
        form = TumblrConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        """
           test if that form is not a valid consumer one
        """
        form = TumblrConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_TUMBLR_KEY)


class ServiceTumblrTest(TumblrTest):

    def setUp(self):
        super(ServiceTumblrTest, self).setUp()
        self.data = {'title': 'a title post', 'content': 'content of the post'}
        self.token = 'QWERTY123#TH#12345'
        self.trigger_id = 1
        self.service = ServiceTumblr(self.token)

    def test_read_data(self):
        t = self.create_tumblr()
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'model_name': 'Tumblr',
                       'trigger_id': t.trigger_id})
        self.token = '123#TH#truc'
        se = ServiceTumblr(self.token)
        res = se.read_data(**kwargs)
        self.assertTrue(type(res) is list)

    @patch.object(TumblrRestClient, 'create_text')
    def test_save_data(self, mock1):
        t = self.create_tumblr()

        se = ServiceTumblr(self.token)
        se.save_data(self.trigger_id, **self.data)
        mock1.assert_called_with(blogname=t.blogname,
                                 title=self.data['title'],
                                 body=self.data['content'],
                                 state='published',
                                 tags=t.tag)
