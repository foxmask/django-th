# coding: utf-8
from django.conf import settings
from django.core.cache import caches

from django_th.tests.test_main import MainTest
from django_th.models import ServicesActivated

from mastodon import Mastodon as MastodonAPI

from th_mastodon.models import Mastodon
from th_mastodon.my_mastodon import ServiceMastodon
from th_mastodon.forms import MastodonProviderForm, MastodonConsumerForm

from unittest.mock import patch

cache = caches['django_th']


class MastodonTest(MainTest):

    """
        MastodonTest Model
    """

    def test_get_services_list(self):
        th_service = ('th_mastodon.my_mastodon.ServiceMastodon',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

    def create_masto(self, tooter='foxmask@mamot.fr', timeline='home',
                     tag='mastodon', fav=False, since_id=1, max_id=0):
        trigger = self.create_triggerservice(consumer_name='ServiceMastodon')
        ServicesActivated.objects.get(name='ServiceMastodon')
        resu = Mastodon.objects.create(tooter=tooter, timeline=timeline,
                                       tag=tag, fav=fav, since_id=since_id,
                                       max_id=max_id,
                                       trigger=trigger, status=True)
        return resu

    def test_mastodon(self):
        m = self.create_masto()
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


class ServiceMastodonTest(MastodonTest):
    """
       ServiceTwitterTest
    """

    def setUp(self):
        super(ServiceMastodonTest, self).setUp()
        self.data = {'text': 'something #thatworks'}
        self.token = 'AZERTY1234'
        self.trigger_id = 1
        self.service = ServiceMastodon(self.token)
    """
    def test_read_data_tooter(self):
        search = {'id': 1}
        t = self.create_masto(since_id=0, tag='')
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'model_name': 'Mastodon',
                       'trigger_id': t.trigger_id,
                       'user': 'foxmask'})
        user_id = []
        user_id[0]['id'] = 1
        with patch.object(MastodonAPI, 'account_statuses') as mock1:
            se = ServiceMastodon(self.token)
            with patch.object(MastodonAPI, 'account_search') as mock2:
                se.read_data(**kwargs)
                mock2.assert_called_with(q='foxmask@mamot.fr')
                mock2.return_value = user_id[0]['id']
        mock1.assert_called_once_with(**search)
    """
    @patch.object(MastodonAPI, 'favourites')
    def test_read_data_fav(self, mock1):
        search = {'max_id': 0, 'since_id': 1}
        t = self.create_masto(tag='', fav=True)
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'model_name': 'Mastodon',
                       'trigger_id': t.trigger_id,
                       'user': 'foxmask'})

        se = ServiceMastodon(self.token)
        se.read_data(**kwargs)
        mock1.assert_called_with(**search)

    @patch.object(MastodonAPI, 'search')
    def test_read_data_tag(self, mock1):
        search = {'q': 'mastodon', 'since_id': 1}
        t = self.create_masto()
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'model_name': 'Mastodon',
                       'trigger_id': t.trigger_id,
                       'user': 'foxmask'})

        se = ServiceMastodon(self.token)
        se.read_data(**kwargs)
        mock1.assert_called_with(**search)

    @patch.object(MastodonAPI, 'status_post')
    def test_save_data_toot(self, mock1):
        self.create_masto()
        token = self.token
        trigger_id = self.trigger_id
        kwargs = {'user': 1}
        self.data['title'] = 'Toot from'
        self.data['link'] = 'http://domain.ltd'

        content = str("{title} {link}").format(
            title=self.data.get('title'),
            link=self.data.get('link'))
        content += ' #mastodon'
        self.data['content'] = content

        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))

        se = ServiceMastodon(self.token, **kwargs)
        se.save_data(trigger_id, **self.data)
        mock1.assert_called_with(content, media_ids=None)

    """
    @patch.object(MastodonAPI, 'status_post')
    @patch.object(MastodonAPI, 'media_post')
    @patch.object(ServiceMastodon, 'media_in_content')
    def test_save_data_toot_media(self, mock1, mock2, mock3):
        self.create_masto()
        token = self.token
        trigger_id = self.trigger_id
        kwargs = {'user': 1}
        self.data['title'] = 'Tweet from xxxx'
        self.data['link'] = 'http://domain.ltd'

        content = ' https://pbs.twimg.com/media/foobar.jpg '

        local_file = os.path.dirname(__file__) + '/../cache/foobar.jpg'
        self.data['content'] = content

        content += str("{link} #mastodon").format(
             link=self.data.get('link'))

        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('text', self.data)
        self.assertNotEqual(self.data['text'], '')

        se = ServiceMastodon(self.token, **kwargs)
        se.save_data(trigger_id, **self.data)
        mock1.assert_called_with(content)
        mock1.return_value = (content, local_file)
        mock2.assert_called_with(content)
        mock2.return_value = 1234  # fake media id
        mock3.assert_called_with(content)
    """
    def test_auth(self):
        pass

    def test_callback(self):
        pass
