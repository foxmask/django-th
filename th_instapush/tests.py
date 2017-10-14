# coding: utf-8
from unittest.mock import patch
from instapush import App
from django_th.tests.test_main import MainTest

from th_instapush.models import Instapush as InstapushModel
from th_instapush.forms import InstapushConsumerForm
from th_instapush.my_instapush import ServiceInstapush


class InstapushTest(MainTest):

    """
        InstapushTest Model
    """

    def setUp(self):
        """
           create a user
        """
        super(InstapushTest, self).setUp()
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else',
                     'content': 'foobar',
                     'summary_detail': 'summary foobar',
                     'description': 'description foobar'}
        self.token = 'AZERTY123'
        self.trigger_id = 1
        self.service = ServiceInstapush(self.token)

    def create_instapush(self):
        """
            Create a Instapush object related to the trigger object
        """
        trigger = self.create_triggerservice(consumer_name='ServiceInstapush')
        event_name = 'signups'
        tracker_name = 'email'
        status = True
        return InstapushModel.objects.create(trigger=trigger,
                                             app_id='1234',
                                             app_secret='k33p1ts3cr3t',
                                             event_name=event_name,
                                             tracker_name=tracker_name,
                                             status=status)

    def test_instapush(self):
        """
           Test if the creation of the Instapush object looks fine
        """
        d = self.create_instapush()
        self.assertTrue(isinstance(d, InstapushModel))
        self.assertEqual(d.show(), "My Instapush %s" % d.name)
        self.assertEqual(d.__str__(), "%s" % d.name)

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_instapush()
        data = {'event_name': d.event_name, 'tracker_name': d.tracker_name,
                'app_id': d.app_id, 'app_secret': d.app_secret}
        form = InstapushConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_read_data(self):
        """
           Test if the creation of the Instapush object looks fine
        """
        kwargs = {}
        se = ServiceInstapush()
        res = se.read_data(**kwargs)
        self.assertTrue(type(res) is dict)

    @patch.object(App, 'notify')
    def test_save_data(self, mock1):
        """
           Test if the creation of the Instapush object looks fine
        """
        self.create_instapush()
        data = {'title': 'foo', 'content': 'bar'}
        se = ServiceInstapush(self.token)
        the_return = se.save_data(self.trigger_id, **data)
        mock1.assert_called_once_with(event_name='signups',
                                      trackers={'email': data['content']})

        self.assertTrue(the_return)
