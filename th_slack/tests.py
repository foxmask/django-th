# coding: utf-8
from django.conf import settings

from th_slack.models import Slack
from th_slack.forms import SlackConsumerForm
from th_slack.my_slack import ServiceSlack

from django_th.tests.test_main import MainTest
from unittest.mock import patch
import requests


class SlackTest(MainTest):

    def create_slack(self):
        trigger = self.create_triggerservice(consumer_name='ServiceSlack',
                                             provider_name='ServiceRss')
        name = 'TriggerHappy Slack'
        url = 'https://hooks.slack.com/services/smth/else/matter'
        status = True
        return Slack.objects.create(name=name,
                                    webhook_url=url,
                                    channel='triggerhappy',
                                    team_id='A0001',
                                    slack_token='ADEPARTPOUSANSSUR',
                                    trigger=trigger,
                                    status=status)


class SlackModelTest(SlackTest):
    """
        SlackModelTest Model
    """

    def test_slack(self):
        r = self.create_slack()
        self.assertTrue(isinstance(r, Slack))
        self.assertEqual(
            r.show(),
            "Services Slack %s %s" % (r.trigger, r.webhook_url)
        )
        self.assertEqual(r.__str__(), r.webhook_url)


class SlackFormTest(SlackTest):
    """
        SlackFormTest
    """

    def test_valid_provider_form(self):
        r = self.create_slack()
        data = {'webhook_url': r.webhook_url,
                'channel': r.channel,
                'team_id': r.team_id,
                'slack_token': r.slack_token}
        form = SlackConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th_cache(self):
        self.assertIn('th_slack', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_slack.my_slack.ServiceSlack',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)


class ServiceSlackTest(SlackTest):

    def setUp(self):
        super(ServiceSlackTest, self).setUp()
        self.sl = self.create_slack()
        self.data = {'subject': 'foobar test',
                     'content': 'a content to publish on slack',
                     'permalink': 'https://domain.tld/new/post/etc/',
                     'type_action': 'create'}

    @patch.object(requests, 'post')
    def test_save_data(self, mock1):
        sl = ServiceSlack()
        sl.save_data(self.sl.trigger_id, **self.data)
        mock1.assert_called_once()

    def test_read_data(self):
        sl = ServiceSlack()
        data = {'trigger_id': self.sl.trigger_id}
        sl.read_data(**data)
