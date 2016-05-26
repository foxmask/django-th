# coding: utf-8
from django.conf import settings
from th_github.models import Github
from th_github.forms import GithubProviderForm, GithubConsumerForm
from django_th.tests.test_main import MainTest


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
