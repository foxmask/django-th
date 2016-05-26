# coding: utf-8
from django.conf import settings
from th_trello.models import Trello
from th_trello.forms import TrelloProviderForm, TrelloConsumerForm
from django_th.tests.test_main import MainTest


class TrelloTest(MainTest):

    """
        TrelloTest Model
    """

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_TRELLO)
        self.assertIn('consumer_key', settings.TH_TRELLO)
        self.assertIn('consumer_secret', settings.TH_TRELLO)

    def test_get_config_th_cache(self):
        self.assertIn('th_trello', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_trello.my_trello.ServiceTrello',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)

    def create_trello(self):
        trigger = self.create_triggerservice(consumer_name='ServiceTrello')
        board_name = 'Trigger Happy'
        list_name = 'To Do'
        status = True
        return Trello.objects.create(trigger=trigger,
                                     board_name=board_name,
                                     list_name=list_name,
                                     status=status)

    def test_trello(self):
        t = self.create_trello()
        self.assertTrue(isinstance(t, Trello))
        self.assertEqual(t.show(), "My Trello %s %s %s" % (t.board_name,
                                                           t.list_name,
                                                           t.card_title))
        self.assertEqual(t.__str__(), "%s %s %s" % (t.board_name,
                                                    t.list_name,
                                                    t.card_title))

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        t = self.create_trello()
        data = {'board_name': t.board_name, 'list_name': t.list_name}
        form = TrelloProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = TrelloProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        t = self.create_trello()
        data = {'board_name': t.board_name, 'list_name': t.list_name}

        form = TrelloConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        form = TrelloConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_read_data(self):
        r = self.create_trello()
        from th_trello.my_trello import ServiceTrello
        kwargs = {'trigger_id': r.trigger_id}
        t = ServiceTrello()
        t.read_data(**kwargs)
        data = list()
        self.assertTrue(type(data) is list)
        self.assertTrue('trigger_id' in kwargs)

    """def test_process_data(self):
        r = self.create_trello()
        from th_trello.my_trello import ServiceTrello

        kwargs = {'trigger_id': r.trigger_id}

        self.assertTrue('trigger_id' in kwargs)

        kw = {'cache_stack': 'th_trello',
              'trigger_id': str(kwargs['trigger_id'])}

        self.assertTrue('cache_stack' in kw)
        self.assertTrue('trigger_id' in kw)

        s = ServiceTrello()
        data = s.process_data(**kw)

        self.assertTrue(type(data) is list)"""
