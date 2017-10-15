from django_th.models import ServicesActivated
from django_th.tests.test_main import MainTest
from django_th.templatetags.django_th_extras import service_readable_class, \
    service_readable, trigger_disabled


class TemplateTagsTest(MainTest):

    def test_service_readable_class(self):
        self.create_triggerservice(consumer_name="ServiceWallabag",
                                   status=True)
        service = ServicesActivated.objects.get(name="ServiceWallabag")
        self.assertTrue(type(service_readable_class(service)) is str)

    def test_service_readable(self):
        self.create_triggerservice(consumer_name="ServiceWallabag",
                                   status=True)
        service = ServicesActivated.objects.get(name="ServiceWallabag")
        self.assertTrue('Service' not in service_readable(service))

    def test_trigger_disabled(self):
        trigger = self.create_triggerservice(service_status=False)
        self.assertTrue(type(trigger_disabled(trigger)) is str)

    def test_trigger_disabled2(self):
        trigger = self.create_triggerservice(consumer_name="ServiceWallabag",
                                             status=False,
                                             service_status=True)
        self.assertTrue(type(trigger_disabled(trigger)) is str)
