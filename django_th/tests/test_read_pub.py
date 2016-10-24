# coding: utf-8
from unittest.mock import patch

from django_th.tests.test_main import MainTest
from django_th.publish import Pub
from django_th.read import Read


class PublishTestCase(MainTest):

    @patch.object(Pub, 'consumer')
    def test_publishing(self, mock1):
        service = self.create_triggerservice()
        p = Pub()
        p.publishing(service)
        mock1.assert_called_once()


class ReadTestCase(MainTest):

    @patch.object(Read, 'provider')
    def test_publishing(self, mock1):
        service = self.create_triggerservice()
        r = Read()
        r.reading(service)
        mock1.assert_called_once()
