# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django_th.models import TriggerService, UserService, ServicesActivated


class MainTest(TestCase):

    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True,
                              consumer_name="ServiceEvernote"):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name=consumer_name, status=True,
            auth_required=True, description='Service Evernote')
        provider = UserService.objects.create(user=user,
                                              token="",
                                              name=service_provider)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_consumer)
        return TriggerService.objects.create(id=1,
                                             provider=provider,
                                             consumer=consumer,
                                             user=user,
                                             date_created=date_created,
                                             description=description,
                                             status=status)
