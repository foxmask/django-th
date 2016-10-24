# coding: utf-8
from unittest.mock import patch
import requests

from django.conf import settings

from django_th.tests.test_main import MainTest

from th_wallabag.models import Wallabag
from th_wallabag.forms import WallabagProviderForm, WallabagConsumerForm
from th_wallabag.my_wallabag import ServiceWallabag

from wallabag_api.wallabag import Wallabag as Wall


class WallabagTest(MainTest):

    """
        wallabagTest Model
    """

    def setUp(self):
        super(WallabagTest, self).setUp()
        self.token = 'AZERTY1234'
        self.trigger_id = 1
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else'}

    def test_wallabag(self):
        """
           Test if the creation of the wallabag object looks fine
        """
        t = self.create_triggerservice()
        d = self.create_wallabag(t)
        self.assertTrue(isinstance(d, Wallabag))
        self.assertEqual(d.show(), "My Wallabag %s" % d.url)
        self.assertEqual(d.__str__(), "%s" % d.url)

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        t = self.create_triggerservice()
        d = self.create_wallabag(t)

        data = {'url': d.url}
        form = WallabagProviderForm(data=data)
        self.assertTrue(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        t = self.create_triggerservice()
        d = self.create_wallabag(t)

        data = {'url': d.url}
        form = WallabagConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th_cache(self):
        self.assertIn('th_wallabag', settings.CACHES)


class ServiceWallabagTest(WallabagTest):

    def setUp(self):
        super(ServiceWallabagTest, self).setUp()

    def test_read_data(self):
        self.create_triggerservice()
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'user': self.user,
                       'model_name': 'Wallabag'})
        self.token = 'AZERTY1234'

        params = dict({'access_token': self.token,
                       'archive': 0,
                       'star': 0,
                       'delete': 0,
                       'sort': 'created',
                       'order': 'desc',
                       'page': 1,
                       'perPage': 30,
                       'tags': []})

        with patch.object(requests, 'get') as mock_read_data:
            mock_read_data.return_value.status_code = 200
            se = ServiceWallabag(self.token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with('http://localhost/api'
                                               '/entries.json', params=params)

    def test_refresh_token(self):
        self.create_triggerservice()
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'user': self.user,
                       'model_name': 'Wallabag'})
        with patch.object(Wall, 'get_token') as mock_get_token:
            se = ServiceWallabag(self.token, **kwargs)
            se._refresh_token()
        mock_get_token.assert_called_once_with(client_id='',
                                               client_secret='',
                                               host='http://localhost',
                                               password='',
                                               username='')

    def test_save_data(self):
        self.create_triggerservice()
        kwargs = {'title': 'foobar', 'link': 'https://google.com'}
        with patch.object(ServiceWallabag, 'new_wall') as mock_save_data:
            se = ServiceWallabag(self.token)
            se.save_data(self.trigger_id, **kwargs)
        mock_save_data.assert_called_once_with(self.token)
