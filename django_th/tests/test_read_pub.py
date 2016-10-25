# coding: utf-8
from unittest.mock import patch
import arrow
from django.conf import settings

from django_th.service_provider import ServiceProvider
from django_th.read import Read
from django_th.publish import Pub
from django_th.tests.test_main import MainTest


class PublishTestCase(MainTest):

    def test_publishing(self):
        service = self.create_triggerservice()
        with patch.object(Pub, 'provider') as mock_pub:
            se = Pub()
            se.publishing(service)
        mock_pub.assert_called_once_with(service)


class ReadTestCase(MainTest):

    def test_reading(self):
        from django_th.services import default_provider
        now = arrow.utcnow().to(settings.TIME_ZONE).format(
            'YYYY-MM-DD HH:mm:ssZZ')
        service = self.create_triggerservice()
        date_triggered = service.date_triggered if service.date_triggered \
            else now

        kwargs = {'token': service.provider.token,
                  'trigger_id': service.id,
                  'date_triggered': date_triggered}

        with patch.object(ServiceProvider, 'get_service') as mock_it:
            mock_it.return_value = default_provider.get_service(
                str(service.provider.name.name))
            with patch.object(Read, 'provider') as mock_read:
                se = Read()
                se.reading(service)
            mock_read.assert_called_once_with(mock_it.return_value, **kwargs)
        mock_it.assert_called_with(service.provider.name.name)
