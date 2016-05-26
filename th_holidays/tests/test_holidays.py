# coding: utf-8
import arrow

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_holidays.models import Holidays

from django_th.models import ServicesActivated, UserService, TriggerService


class HolidaysTest(TestCase):

    """
        Holidays Model
    """

    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_holidays(self, status=True, trigger="My first Service"):
        """
            dummy data
        """
        now = arrow.utcnow().to(
            settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ss')
        date_created = now
        user = self.user
        status = True
        service_provider = ServicesActivated.objects.create(
            name='ServiceRss9', status=True,
            auth_required=False, description='Service RSS2')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceEvernote9', status=True,
            auth_required=True, description='Service Evernote2')
        provider = UserService.objects.create(user=user,
                                              token="",
                                              name=service_provider)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_consumer)
        trigger = TriggerService.objects.create(provider=provider,
                                                consumer=consumer,
                                                user=user,
                                                date_created=date_created,
                                                description="My first Service",
                                                status=status)

        return Holidays.objects.create(user=user,
                                       trigger=trigger,
                                       status=status)

    def test_holidays(self):
        h = self.create_holidays()
        self.assertTrue(isinstance(h, Holidays))
        self.assertEqual(h.show(), "Holidays for service {}".format(h.trigger))
        self.assertEqual(h.__str__(), h.trigger)
