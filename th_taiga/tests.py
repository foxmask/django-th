# coding: utf-8
from django.conf import settings

from th_taiga.models import Taiga
from th_taiga.forms import TaigaProviderForm

from django_th.tests.test_main import MainTest


class TaigaTest(MainTest):

    def create_taiga(self):
        trigger = self.create_triggerservice(consumer_name='ServiceSlack',
                                             provider_name='ServiceTaiga')
        name = 'TriggerHappy Taiga'
        webhook_secret_key = 'myverylongsecretkey'
        project_name = 'foxmask-trigger-happy'
        status = True
        return Taiga.objects.create(name=name,
                                    project_name=project_name,
                                    webhook_secret_key=webhook_secret_key,
                                    trigger=trigger,
                                    status=status)


class TaigaModelTest(TaigaTest):
    """
        TaigaModelTest Model
    """

    def test_taiga(self):
        r = self.create_taiga()
        self.assertTrue(isinstance(r, Taiga))
        self.assertEqual(
            r.show(),
            "Services Taiga %s" % r.trigger
        )
        self.assertEqual(r.__str__(), r.trigger.__str__())


class TaigaFormTest(TaigaTest):
    """
        TaigaFormTest
    """

    def test_valid_provider_form(self):
        data = {'project_name': 'foxmask-trigger-happy',
                'webhook_secret_key': '123'}
        form = TaigaProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_get_config_th_cache(self):
        self.assertIn('th_taiga', settings.CACHES)

    def test_get_services_list(self):
        th_service = ('th_taiga.my_taiga.ServiceTaiga',)
        for service in th_service:
            self.assertIn(service, settings.TH_SERVICES)
