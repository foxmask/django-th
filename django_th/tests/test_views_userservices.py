import unittest
from django.test import RequestFactory
from django.contrib.auth.models import User

from django_th.views_userservices import UserServiceListView
from django_th.models import UserService
from django_th.tests.test_views import setup_view


class UserServiceListViewTestCase(unittest.TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def test_context_data(self):
        # Setup request and view
        queryset = UserService.objects.all()

        request = self.factory.get('/')
        request.user = self.user

        view = UserServiceListView(
            template_name='services/services.html',
            context_object_name="services_list",
            object_list=queryset)
        view = setup_view(view, request)

        context = view.get_context_data()

        if request.user.is_authenticated():
            nb_user_service = nb_service = 20
            context, action = self.get_action_context(context,
                                                      nb_user_service,
                                                      nb_service)
            self.assertEqual(context['action'], action)

            nb_user_service = 19
            nb_service = 20
            context, action = self.get_action_context(context,
                                                      nb_user_service,
                                                      nb_service)
            self.assertEqual(context['action'], action)

    def get_action_context(self, context, nb_user_service, nb_service):
        if nb_user_service == nb_service:
            context['action'] = 'hide'
            action = 'hide'
        else:
            context['action'] = 'display'
            action = 'display'

        return context, action
