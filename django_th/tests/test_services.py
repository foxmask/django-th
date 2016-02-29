# coding: utf-8
import uuid

from django.contrib.auth.models import User

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

from django_th.services.services import ServicesMgr
from django_th.tests.test_main import MainTest

from th_rss.models import Rss


class ServicesMgrTestCase(MainTest):

    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')
        self.create_rss()

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True,
                              consumer_name="ServiceEvernote"):
        return super(ServicesMgrTestCase, self).create_triggerservice(self)

    def create_rss(self, **kwargs):
        trigger = self.create_triggerservice()
        name = 'Foobar RSS'
        url = 'http://foobar.com/somewhere/in/the/rainbow.rss'
        status = True
        return Rss.objects.create(uuid=uuid.uuid4(),
                                  url=url,
                                  name=name,
                                  trigger=trigger,
                                  status=status)

    def test_set_title(self):
        data = {'title': 'foobar'}
        self.assertTrue('title' in data)
        data = {'link': 'http://localhost/url/to/news'}
        self.assertTrue('title' not in data)
        self.assertTrue('link' in data)

    def test_set_content(self):
        data = {'summary_detail': 'some summary'}
        self.assertTrue('summary_detail' in data)
        data = {'description': 'foobar'}
        self.assertTrue('description' in data)
        self.assertTrue('summary_detail' not in data)

    def test_read_data(self, **kwargs):
        kwargs = {'model_name': 'Rss', 'trigger_id': 1}
        self.assertTrue('model_name', kwargs)
        self.assertTrue('trigger_id', kwargs)

        model = get_model('django_th', kwargs['model_name'])
        result = model.objects.get(trigger_id=kwargs['trigger_id'])
        self.assertTrue(isinstance(result, Rss))

    def test_process_data(self, **kwargs):
        kwargs = {'cache_stack': 'th_rss', 'trigger_id': '1'}
        self.assertTrue('cache_stack' in kwargs)

    def _set_title(self, data):
        return data['title'] if 'title' in data else data['link']

    def _set_content(self, data):
        return data['summary_detail'] if 'summary_detail' in data else data['description']

    def test_save_data(self, **kwargs):
        data = {'title': 'a title', 'summary_detail': 'a content'}
        s = ServicesMgr('')
        title = s.set_title(data)
        content = s.set_content(data)
        self.assertTrue(title)
        self.assertTrue(content)
