# coding: utf-8
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.contrib.auth.models import User

from django_th.tests.test_main import MainTest
from th_todoist.models import Todoist
from th_todoist.forms import TodoistProviderForm, TodoistConsumerForm
from th_todoist.my_todoist import ServiceTodoist


class TodoistTest(MainTest):

    def test_get_config_th_cache(self):
        self.assertIn('th_todoist', settings.CACHES)

    """
        TodoistTest Model
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

        self.token = 'AZERTY123'
        self.trigger_id = 1
        self.service = ServiceTodoist(self.token)

    def create_todoist(self):
        """
            Create a Todoist object related to the trigger object
        """
        trigger = self.create_triggerservice(consumer_name="SerivceTodoist")
        name = 'todoist'
        status = True
        return Todoist.objects.create(trigger=trigger, name=name, status=status)

    def test_todoist(self):
        """
           Test if the creation of the todoist object looks fine
        """
        d = self.create_todoist()
        self.assertTrue(isinstance(d, Todoist))
        self.assertEqual(d.show(), "My Todoist %s" % d.name)
        self.assertEqual(d.__str__(), "%s" % d.name)

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_todoist()
        data = {'name': d.name}
        form = TodoistProviderForm(data=data)
        self.assertTrue(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_todoist()
        data = {'name': d.name}
        form = TodoistConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_TODOIST)

    def test_read_data(self):
        """
           Test if the creation of the Todoist object looks fine
        """
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'model_name': 'Todoist'})

        with patch.object(ServiceTodoist, 'read_data') as mock_read_data:
            se = ServiceTodoist(self.token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with(**kwargs)

    def test_save_data(self):
        """
           Test if the creation of the Todoist object looks fine
        """
        self.create_todoist()
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'foobar'}

        self.service.save_data = MagicMock(name='save_data')
        the_return = self.service.save_data(self.trigger_id, **data)

        self.assertTrue(the_return)
