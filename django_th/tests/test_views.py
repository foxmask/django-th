# coding: utf-8
from django.core.cache import caches
from django.test import RequestFactory, Client

from django_th.models import TriggerService
from django_th.views import TriggerEditedTemplateView
from django_th.views import TriggerDeletedTemplateView, TriggerListView
from django_th.views_fbv import can_modify_trigger, trigger_on_off, \
    trigger_edit, trigger_switch_all_to, list_services, \
    service_related_triggers_switch_to, fire_trigger
from django_th.tests.test_main import MainTest, setup_view

from th_rss.models import Rss

import unittest
import uuid

cache = caches['django_th']


class TriggerEditedTemplateViewTestCase(unittest.TestCase):

    def test_get(self):
        template = "triggers/edited_thanks_trigger.html"
        # Setup request and view.
        request = RequestFactory().get('/th/trigger/edit/thanks')
        view = TriggerEditedTemplateView.as_view(template_name=template)
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'triggers/edited_thanks_trigger.html')


class TriggerDeletedTemplateViewTestCase(unittest.TestCase):

    def test_get(self):
        template = "triggers/deleted_thanks_trigger.html"
        # Setup request and view.
        request = RequestFactory().get('/th/trigger/delete/thanks')
        view = TriggerDeletedTemplateView.as_view(template_name=template)
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'triggers/deleted_thanks_trigger.html')


class TriggerListViewTestCase(MainTest):

    def setUp(self):
        super(TriggerListViewTestCase, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_context_data(self):
        """
        TriggerListView.get_context_data() sets
        'triggers_enabled', 'triggers_disabled', 'services_activated'
        in context.
        """
        # Setup name.
        triggers_enabled = triggers_disabled = services_activated = 0
        queryset = TriggerService.objects.all()

        # Setup request and view.
        request = self.factory.get('/')
        request.user = self.user

        view = TriggerListView(
            template_name='home.html', object_list=queryset)
        view = setup_view(view, request)
        # Run.
        if request.user.is_authenticated():
            triggers_enabled = 3
            triggers_disabled = 1
            services_activated = 5

        context = view.get_context_data()
        context['nb_triggers'] = {
            'enabled': triggers_enabled, 'disabled': triggers_disabled}
        context['nb_services'] = services_activated

        # Check.
        self.assertEqual(context['nb_triggers']['enabled'], triggers_enabled)
        self.assertEqual(context['nb_triggers']['disabled'], triggers_disabled)
        self.assertEqual(context['nb_services'], services_activated)


class ViewFunction(MainTest):

    def setUp(self):
        super(ViewFunction, self).setUp()
        self.request = RequestFactory().get('/')

    def test_can_modify_trigger(self):
        self.assertFalse(can_modify_trigger(self.request, provider='ServiceRss',
                                            consumer='ServiceTwitter'))
        # self.assertTrue(can_modify_trigger(request, consumer='', provider=''))

    def test_logout(self):
        c = Client()
        c.logout()

    def test_trigger_on_off(self):
        t = self.create_triggerservice()
        response = trigger_on_off(request=self.request, trigger_id=t.id)
        self.assertTrue(response.status_code, 200)
        TriggerService.objects.filter(id=t.id).update(status=False)

        response = trigger_on_off(request=self.request, trigger_id=t.id)
        self.assertTrue(response.status_code, 200)

    def test_fire_trigger(self):
        service = self.create_triggerservice()
        name = 'TriggerHappy RSS'
        url = 'https://blog.trigger-happy.eu/feeds/all.rss.xml'
        status = True
        Rss.objects.create(uuid=uuid.uuid4(), url=url, name=name,
                           trigger=service, status=status)
        cache.set('django_th_fire_trigger_1', '*')
        response = fire_trigger(self.request, 1)
        self.assertTrue(response.status_code, 200)
        cache.delete('django_th_fire_trigger_1')
        response = fire_trigger(self.request, 1)
        self.assertTrue(response.status_code, 200)

    def test_service_related_triggers_switch_to(self):
        user_service_id = 1
        response = service_related_triggers_switch_to(self.request,
                                                      user_service_id, 'off')
        self.assertEqual(response.status_code, 302)
        response = service_related_triggers_switch_to(self.request,
                                                      user_service_id, 'on')
        self.assertEqual(response.status_code, 302)

    def test_trigger_switch_all_to(self):
        self.request.user = self.user

        response = trigger_switch_all_to(self.request, 'off')
        self.assertEqual(response.status_code, 302)

        response = trigger_switch_all_to(self.request, 'on')
        self.assertEqual(response.status_code, 302)

    def test_list_services(self):
        self.create_triggerservice()

        self.request.id = 1

        data = list_services(self.request, step='0')
        self.assertTrue(len(data) > 0)

        data = list_services(self.request, step='3')
        self.assertTrue(len(data) > 0)

    def test_trigger_edit_failed(self):
        trigger_id = 1
        edit_what = 'blackhole'
        response = trigger_edit(self.request, trigger_id, edit_what)

        self.assertEqual(response.status_code, 302)

    def test_trigger_edit(self):
        trigger = self.create_triggerservice()

        edit_what = 'Consumer'
        response = trigger_edit(self.request, trigger.id, edit_what)
        self.assertEqual(response.status_code, 200)

        edit_what = 'Provider'

        url = 'https://blog.trigger-happy.eu/feeds/all.rss.xml'
        self.uuid = uuid.uuid4()
        Rss.objects.create(uuid=self.uuid,
                           url=url,
                           name='TriggerHappy RSS',
                           trigger=trigger,
                           status=True)

        response = trigger_edit(self.request, trigger.id, edit_what)
        self.assertEqual(response.status_code, 200)

        self.request.method = 'POST'
        response = trigger_edit(self.request, trigger.id, edit_what)
        self.assertEqual(response.status_code, 200)
