# coding: utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory


from django_th.forms.base import UserServiceForm
from django_th.models import UserService, ServicesActivated
from django_th.tests.test_main import MainTest, setup_view
from django_th.views_userservices import UserServiceListView, UserServiceCreateView, UserServiceUpdateView


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


class UserServiceCreateViewTestCase(MainTest):

    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')
        ServicesActivated.objects.create(name='ServiceRss', status=True, auth_required=False, description='Service RSS')

    def test_get(self):
        template_name = 'services/service_form.html'
        # Setup request and view.
        request = RequestFactory().get('th/service/add/')
        request.user = self.user
        view = UserServiceCreateView.as_view(template_name=template_name)
        # Run.
        response = view(request, user=request.user, service_name="ServiceRss")
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], template_name)

    def test_valid_form(self):
        data = {'duration': 'n'}
        form = UserServiceForm(data=data, initial={'user': self.user, 'name': 'ServiceRss'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'duration': 'x'}
        form = UserServiceForm(data=data, initial={'user': self.user, 'name': 'ServiceRss'})
        self.assertFalse(form.is_valid())


class UserServiceUpdateViewTestCase(MainTest):

    def test_get(self):
        template_name = 'services/service_form.html'
        t = self.create_triggerservice()
        # Setup request and view.
        request = RequestFactory().get('th/service/edit/')
        request.user = self.user
        view = UserServiceUpdateView.as_view(template_name=template_name)
        # Run.
        response = view(request, user=request.user, pk=t.id)
        # Check.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], template_name)
