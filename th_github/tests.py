# coding: utf-8
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.core.cache import caches

from th_github.models import Github
from th_github.forms import GithubProviderForm, GithubConsumerForm
from th_github.my_github import ServiceGithub
from django_th.tests.test_main import MainTest

cache = caches['th_github']


class GithubTest(MainTest):

    def create_github(self):
        """
            Create a github object related to the trigger object
        """
        trigger = self.create_triggerservice(consumer_name='ServiceGithub')
        name = 'github'
        repo = 'foobar'
        project = 'barfoo'
        status = True
        return Github.objects.create(trigger=trigger,
                                     name=name,
                                     status=status,
                                     repo=repo,
                                     project=project)

    def test_github(self):
        """
           Test if the creation of the github object looks fine
        """
        d = self.create_github()
        self.assertTrue(isinstance(d, Github))
        self.assertEqual(d.show(), "My Github {}".format(d.name))
        self.assertEqual(d.__str__(), d.name)

    """
        Form
    """
    # provider

    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_github()
        data = {'repo': d.repo, 'project': d.project}
        form = GithubProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        """
           test if that form is not a valid provider one
        """
        form = GithubProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_github()
        data = {'repo': d.repo, 'project': d.project}
        form = GithubConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        """
           test if that form is not a valid consumer one
        """
        form = GithubConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_GITHUB)

    def test_get_config_th_cache(self):
        self.assertIn('th_github', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_github.my_github.ServiceGithub',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)


class ServiceGithubTest(GithubTest):
    """
       ServiceGithubTest
    """
    def setUp(self):
        super(ServiceGithubTest, self).setUp()
        self.data = {'content': 'this is the body of the issue;)',
                     'summary_detail': 'a nice issue ;)',
                     'title': 'a nice issue ;)',
                     'description': 'this is the body of the issue'}
        self.token = 'QWERTY123#TH#12345'
        self.trigger_id = 1
        self.service = ServiceGithub(self.token)

    def test_read_data(self):
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'trigger_id': self.trigger_id,
                       'model_name': 'Github'})

        # date_triggered = kwargs.get('date_triggered')
        trigger_id = kwargs.get('trigger_id')

        kwargs['model_name'] = 'Github'

        data = []
        cache.set('th_github_' + str(trigger_id), data)

        with patch.object(ServiceGithub, 'read_data') as mock_read_data:
            se = ServiceGithub(self.token)
            se.read_data(**kwargs)
        mock_read_data.assert_called_once_with(**kwargs)

    def test_save_data(self):
        token = self.token
        trigger_id = self.trigger_id

        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('content', self.data)
        self.assertIn('summary_detail', self.data)
        self.assertIn('description', self.data)
        self.assertIn('title', self.data)
        self.assertNotEqual(self.data['title'], '')

        self.service.save_data = MagicMock(name='save_data')
        the_return = self.service.save_data(trigger_id, **self.data)

        self.assertTrue(the_return)
