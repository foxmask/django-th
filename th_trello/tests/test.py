# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from th_trello.models import Trello
from django_th.models import TriggerService, UserService, ServicesActivated
from th_trello.forms import TrelloProviderForm, TrelloConsumerForm


class TrelloTest(TestCase):

    """
        TrelloTest Model
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
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceTrello', status=True,
            auth_required=True, description='Service Trello')
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

    def create_trello(self):
        trigger = self.create_triggerservice()
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
