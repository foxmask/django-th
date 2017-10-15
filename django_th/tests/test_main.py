# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django_th.models import TriggerService, UserService, ServicesActivated
from th_wallabag.models import Wallabag


class MainTest(TestCase):
    """

    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_wallabag(self, trigger):
        return Wallabag.objects.create(trigger=trigger,
                                       url='https://trigger-happy.eu',
                                       tag='test', title='title test')

    def create_triggerservice(self, trigger_id=1, date_created="20130610",
                              description="My first Service", status=True,
                              consumer_name="ServiceWallabag",
                              provider_name="ServiceRss",
                              service_status=True,
                              duration='d'):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name=provider_name, status=service_status,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name=consumer_name, status=service_status,
            auth_required=False, description='Service Wallabag')
        provider = UserService.objects.create(user=user,
                                              token="",
                                              name=service_provider,
                                              duration=duration)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              host='http://localhost',
                                              name=service_consumer,
                                              duration=duration)
        trigger = TriggerService.objects.create(id=trigger_id,
                                                provider=provider,
                                                consumer=consumer,
                                                user=user,
                                                date_created=date_created,
                                                description=description,
                                                status=status)
        self.create_wallabag(trigger)
        return trigger


def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns view instance.

    args and kwargs are the same you would pass to ``reverse()``

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
