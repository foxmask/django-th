# coding: utf-8
from django.core.urlresolvers import reverse
from django.test import RequestFactory

from django_th.models import UserService
from django_th.tests.test_views import setup_view
from django_th.tests.test_main import MainTest
from django_th.views_userservices import UserServiceListView


class UserServiceListViewTestCase(MainTest):

    def setUp(self):
        super(UserServiceListViewTestCase, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_context_data(self):
        # Setup request and view
        queryset = UserService.objects.all()

        request = self.factory.get(reverse('user_services'))
        request.user = self.user

        response = UserServiceListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        view = UserServiceListView(
            template_name='services/services.html',
            context_object_name="services_list",
            object_list=queryset)
        view = setup_view(view, request)

        context = view.get_context_data()
        self.assertIn('service_list_remaining', context)


"""
class UserServiceCreateViewTestCase(MainTest):

    def setUp(self):
        super(UserServiceCreateViewTestCase, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_context_data(self):
        # Setup request and view
        request = self.factory.get(reverse('add_service', args=['ServiceRss']))
        request.user = self.user

        view = UserServiceCreateView(
            template_name='services/service_form.html',
            form_class=UserServiceForm)

        kwargs = dict()
        kwargs['service_name'] = 'ServiceRss'

        view = setup_view(view, request, **kwargs)
        context = view.get_context_data()

        self.assertIn('service_name_alone', context)
        self.assertIn('service_name', context)
        self.assertIn('SERVICES_AUTH', context)
        self.assertIn('SERVICES_HOSTED_WITH_AUTH', context)
        self.assertIn('SERVICES_NEUTRAL', context)


class UserServiceUpdateViewTestCase(MainTest):

    def setUp(self):
        super(UserServiceUpdateViewTestCase, self).setUp()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_context_data(self):
        # Setup request and view
        request = self.factory.get(reverse('edit_service', args=[1]))
        request.user = self.user

        view = UserServiceUpdateView(
            template_name='services/service_form.html',
            form_class=UserServiceForm)

        kwargs = dict()
        kwargs['pk'] = 1

        view = setup_view(view, request, **kwargs)
        context = view.get_context_data()

        self.assertIn('service_name_alone', context)
        self.assertIn('service_name', context)
        self.assertIn('SERVICES_AUTH', context)
        self.assertIn('SERVICES_HOSTED_WITH_AUTH', context)
        self.assertIn('SERVICES_NEUTRAL', context)
"""
