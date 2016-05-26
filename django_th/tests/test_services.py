# coding: utf-8
import uuid

from django.contrib.auth.models import User

try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    pass

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

    def create_rss(self):
        trigger = self.create_triggerservice()
        name = 'Foobar RSS'
        url = 'https://blog.trigger-happy.eu/feeds/all.rss.xml'
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

    def test_save_data(self):
        data = {'title': 'a title', 'summary_detail': 'a content'}
        s = ServicesMgr('')
        title = s.set_title(data)
        content = s.set_content(data)
        self.assertTrue(title)
        self.assertTrue(content)
