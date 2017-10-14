# coding: utf-8
from unittest.mock import patch
from todoist.api import TodoistAPI

from django.conf import settings

from django_th.tests.test_main import MainTest
from th_todoist.models import Todoist
from th_todoist.forms import TodoistProviderForm, TodoistConsumerForm
from th_todoist.my_todoist import ServiceTodoist


class TodoistTest(MainTest):

    """
        TodoistTest Model
    """
    def setUp(self):
        """
           create a user
        """
        super(TodoistTest, self).setUp()

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
        self.assertTrue(settings.TH_TODOIST_KEY)

    def test_read_data(self):
        """
           Test if the creation of the Todoist object looks fine
        """
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'model_name': 'Todoist'})

        with patch.object(TodoistAPI, 'sync') as mock_read_data:
            se = ServiceTodoist(self.token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with()

    def test_save_data(self):
        """
           Test if the creation of the Todoist object looks fine
        """
        self.create_todoist()
        data = {'link': 'http://foo.bar/some/thing/else/what/else',
                'title': 'what else',
                'content': 'foobar'}
        content = data['title'] + ' ' + data['content'] + ' ' + data['link']
        with patch.object(TodoistAPI, 'add_item') as mock_save_data:
            se = ServiceTodoist(self.token)
            se.save_data(self.trigger_id, **data)
        mock_save_data.assert_called_once_with(content)

    def test_save_data2(self):
        """
           data is empty
        """
        self.create_todoist()
        data = {'link': '',
                'title': '',
                'content': ''}
        se = ServiceTodoist(self.token)
        res = se.save_data(self.trigger_id, **data)
        self.assertFalse(res)

    def test_save_data3(self):
        """
           token is empty
        """
        data = {'link': '',
                'title': '',
                'content': ''}
        self.token = ''
        se = ServiceTodoist(self.token)
        res = se.save_data(self.trigger_id, **data)
        self.assertFalse(res)
