# coding: utf-8
import unittest
from django.test import RequestFactory
from django.contrib.auth.models import User

from django_th.views import TriggerEditedTemplateView
from django_th.views import TriggerDeletedTemplateView
from django_th.views import TriggerListView
from django_th.models import TriggerService


class TriggerEditedTemplateViewTestCase(unittest.TestCase):

    def test_get(self):
        template = "triggers/thanks_trigger.html"
        # Setup request and view.
        request = RequestFactory().get('/th/trigger/edit/thanks')
        view = TriggerEditedTemplateView.as_view(template_name=template)
        sentence = 'Your trigger has been successfully modified'
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'triggers/thanks_trigger.html')
        self.assertEqual(response.context_data['sentence'], sentence)


class TriggerDeletedTemplateViewTestCase(unittest.TestCase):

    def test_get(self):
        template = "triggers/thanks_trigger.html"
        # Setup request and view.
        request = RequestFactory().get('/th/trigger/delete/thanks')
        view = TriggerDeletedTemplateView.as_view(template_name=template)
        sentence = 'Your trigger has been successfully deleted'
        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'triggers/thanks_trigger.html')
        self.assertEqual(response.context_data['sentence'], sentence)


class TriggerListViewTestCase(unittest.TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

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


def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns view instance.

    args and kwargs are the same you would pass to ``reverse()``

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
