# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from django_th.models import TriggerService, UserService, ServicesActivated

from th_reddit.models import Reddit
from th_reddit.my_reddit import ServiceReddit
from th_reddit.forms import RedditProviderForm, RedditConsumerForm


class RedditTest(TestCase):

    """
        redditTest Model
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

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceReddit', status=True,
            auth_required=True, description='Service Reddit')
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

    def create_reddit(self, share_link=False):
        """
            Create a Reddit object related to the trigger object
        """
        trigger = self.create_triggerservice()
        subreddit = 'python'
        status = True
        return Reddit.objects.create(trigger=trigger,
                                     subreddit=subreddit,
                                     share_link=share_link,
                                     status=status)

    def test_reddit(self):
        """
           Test if the creation of the reddit object looks fine
        """
        d = self.create_reddit()
        self.assertTrue(isinstance(d, Reddit))
        self.assertEqual(d.show(), "My Reddit %s" % d.subreddit)

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        """
           test if that form is a valid provider one
        """
        d = self.create_reddit()
        data = {'subreddit': d.subreddit, 'share_link': d.share_link}
        form = RedditProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        """
           test if that form is not a valid provider one
        """
        form = RedditProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        """
           test if that form is a valid consumer one
        """
        d = self.create_reddit()
        data = {'subreddit': d.subreddit, 'share_link': d.share_link}
        form = RedditConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        """
           test if that form is not a valid consumer one
        """
        form = RedditConsumerForm(data={})
        self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_REDDIT_KEY)


class ServiceRedditTest(RedditTest):

    def setUp(self):
        super(ServiceRedditTest, self).setUp()
        self.data = {'text': 'something #thatworks'}
        self.token = 'QWERTY123#TH#12345'
        self.trigger_id = 1
        self.service = ServiceReddit(self.token)
    """
    @patch('praw.Reddit')
    def test_read_data(self, mock1):
        t = self.create_reddit()
        kwargs = dict({'date_triggered': '2013-05-11 13:23:58+00:00',
                       'model_name': 'Reddit',
                       'trigger_id': t.trigger_id})

        se = ServiceReddit(self.token)
        res = se.read_data(**kwargs)
        self.assertTrue(type(res) is bool)
        mock1.assert_called_with(t.subreddit)

    @patch('praw.Reddit')
    def test_save_data(self, mock1):
        t = self.create_reddit()
        token = self.token
        trigger_id = self.trigger_id

        self.data['title'] = 'Toot from'
        self.data['link'] = 'http://domain.ltd'

        content = str("{title} {link}").format(
            title=self.data.get('title'),
            link=self.data.get('link'))

        self.data['content'] = content

        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))

        se = ServiceReddit(self.token)
        res = se.save_data(trigger_id, **self.data)
        self.assertTrue(type(res) is bool)
        mock1.assert_called_with(t.subreddit)

    def test_save_data2(self):
        self.create_reddit()
        data = {'link': '',
                'title': '',
                'content': ''}
        self.token = ''
        se = ServiceReddit(self.token)
        res = se.save_data(self.trigger_id, **data)
        self.assertFalse(res)
    """
    def test_auth(self):
        pass

    def test_callback(self):
        pass
