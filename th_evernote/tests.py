# coding: utf-8
from unittest.mock import patch

from django.conf import settings
from django.core.cache import caches

from django_th.tests.test_main import MainTest
from th_evernote.models import Evernote
from th_evernote.forms import EvernoteProviderForm, EvernoteConsumerForm
from th_evernote.my_evernote import ServiceEvernote
from th_evernote.evernote_mgr import EvernoteMgr
from th_evernote.sanitize import sanitize
from evernote.api.client import EvernoteClient
try:
    from unittest import mock
except ImportError:
    import mock


cache = caches['django_th']


class EvernoteTest(MainTest):

    """
        EvernoteTest Model
    """

    def create_evernote(self):
        trigger = self.create_triggerservice(consumer_name='ServiceEvernote')
        tag = 'test'
        notebook = 'my notebook'
        title = 'a new note'
        status = True
        return Evernote.objects.create(tag=tag, title=title,
                                       notebook=notebook, trigger=trigger,
                                       status=status)


class EvernoteView(EvernoteTest):

    def test_evernote(self):
        ev = self.create_evernote()
        self.assertIsInstance(ev, Evernote)
        self.assertEqual(ev.show(), "My Evernote {}".format(ev.title))
        self.assertEqual(ev.__str__(), ev.title)

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        ev = self.create_evernote()
        data = {'tag': ev.tag, 'notebook': ev.notebook}
        form = EvernoteProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = EvernoteProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        ev = self.create_evernote()
        data = {'tag': ev.tag, 'notebook': ev.notebook}
        form = EvernoteConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        form = EvernoteConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_EVERNOTE_KEY)

    def test_get_services_list(self):
        th_service = ('th_evernote.my_evernote.ServiceEvernote',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)


class ServiceEvernoteTest(EvernoteTest):
    """
       ServiceEvernoteTest
    """

    def setUp(self):
        super(ServiceEvernoteTest, self).setUp()
        self.ev = self.create_evernote()
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else',
                     'content': 'A nice content with a nice '
                                '<a href="http://domain.tld">foobar link</a>',
                     'summary_detail': 'summary foobar',
                     'description': 'description foobar'}
        self.token = 'AZERTY123'
        self.trigger_id = 1
        self.service = ServiceEvernote(self.token)

    def test_read_data(self):
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id})

        with patch.object(EvernoteClient, 'get_note_store') as mock_ev:
            se = ServiceEvernote(self.token)
            se.read_data(**kwargs)
        mock_ev.assert_called_once_with()

    @patch.object(EvernoteClient, 'get_note_store')
    # @patch.object(EvernoteMgr, 'create_note')
    # def test_save_data(self, mock1, mock2):
    def test_save_data(self, mock1):
        self.assertTrue(self.token)
        self.assertIsInstance(self.trigger_id, int)
        self.assertIn('content', self.data)
        self.assertIn('summary_detail', self.data)
        self.assertIn('description', self.data)
        self.assertIn('title', self.data)
        self.assertIsNotNone(self.data['link'])
        self.assertNotEqual(self.data['title'], '')
        self.assertIn('sandbox', settings.TH_EVERNOTE_KEY)

        se = ServiceEvernote(self.token)
        se.save_data(self.trigger_id, **self.data)
        mock1.assert_called_once()
        # mock2.assert_called_once()

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_EVERNOTE_KEY)
        self.assertIn('consumer_key', settings.TH_EVERNOTE_KEY)
        self.assertIn('consumer_secret', settings.TH_EVERNOTE_KEY)
        self.assertIn('sandbox', settings.TH_EVERNOTE_KEY)

    def test_get_evernote_client(self, token=None):
        """
            get the token from evernote
        """
        sandbox = settings.TH_EVERNOTE_KEY['sandbox']
        client = mock.Mock(return_value=True)
        client.method(token=token, sandbox=sandbox)
        client.method.assert_called_with(token=token, sandbox=sandbox)

        sandbox = settings.TH_EVERNOTE_KEY['sandbox']
        consumer_key = settings.TH_EVERNOTE_KEY['consumer_key']
        consumer_secret = settings.TH_EVERNOTE_KEY['consumer_secret']

        client = mock.Mock(return_value=True)
        client.method(consumer_key=consumer_key,
                      consumer_secret=consumer_secret, sandbox=sandbox)
        client.method.assert_called_with(consumer_key=consumer_key,
                                         consumer_secret=consumer_secret,
                                         sandbox=sandbox)

    def test_auth(self):
        pass

    def test_callback(self):
        pass

    def test_sanitize(self):
        html = "<html><body>" \
               "<p>coucou</p>" \
               "<dir>foobar</dir>" \
               "<div data-foobar='nothing'>foobar2</div>" \
               "<a href='ftp://localhost'>dropped</a>" \
               "<a href='http://localhost'>kept</a>" \
               "</body></html>"
        html = sanitize(html)
        self.assertTrue("dir" not in html)
        self.assertTrue("ftp" not in html)
        self.assertTrue("data-foobar" not in html)
        self.assertTrue("http" in html)

    def test_set_header(self):
        header = EvernoteMgr.set_header()
        self.assertTrue('DOCTYPE en-note SYSTEM "http://xml.evernote.'
                        'com/pub/enml2.dtd' in header)

    def test_footer(self):
        content = ''
        se = ServiceEvernote(self.token)
        footer = se._footer(self.ev, self.data, content)
        self.assertIsInstance(footer, str)

    def test_cleaning_content(self):
        se = ServiceEvernote(self.token)
        self.assertIsInstance(se._cleaning_content('foobar'), str)

    def test_set_note_attribute(self):
        data = {}
        attr = EvernoteMgr.set_note_attribute(data)
        self.assertTrue(type(attr) is bool)
        data = {'link': 'http://localhost'}
        attr = EvernoteMgr.set_note_attribute(data)
        self.assertTrue(type(attr) is not bool)
