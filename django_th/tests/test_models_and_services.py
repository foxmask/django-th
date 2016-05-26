# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django_th.models import TriggerService
from django_th.models import UserService, ServicesActivated
from django_th.forms.base import TriggerServiceForm
from django_th.forms.base import UserServiceForm
from django_th.tests.test_main import MainTest


class UserServiceTest(TestCase):

    """
        UserService Model
    """

    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_userservice(self, token="AZERTY12345"):
        user = self.user
        name = ServicesActivated.objects.create(name='ServiceEvernote',
                                                status=True,
                                                auth_required=True,
                                                description='Service Evernote')
        return UserService.objects.create(user=user, token=token, name=name)

    def test_userservice(self):
        u = self.create_userservice()
        self.assertTrue(isinstance(u, UserService))
        self.assertEqual(u.show(), "User Service %s %s %s" % (u.user, u.token,
                                                              u.name))
        self.assertEqual(u.__str__(), u.name.name)

    def test_valid_form(self):
        u = self.create_userservice()
        data = {'user': u.user, 'name': u.name, 'token': ''}
        if u.name.auth_required:
            data = {'user': u.user, 'name': u.name, 'token': u.token}
        initial = {'user': self.user}
        # create a second service to be able to cover the "else" in
        # activated_services()
        user = self.user
        ServicesActivated.objects.create(name='ServiceRss',
                                         status=True,
                                         auth_required=True,
                                         description='Service Rss')
        form = UserServiceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid())
        form.save(user=user)
    """
    def test_invalid_form(self):
        data = {'user': '', 'name': '', 'token': ''}
        initial = {'user': self.user}
        form = UserServiceForm(data=data, initial=initial)
        self.assertFalse(form.is_valid())
    """


class ServicesActivatedTest(TestCase):

    """
        ServicesActivated Model
    """

    def create_servicesactivated(self):
        name = 'ServiceRss'
        status = True
        auth_required = False
        description = 'RSS Feeds Service'
        return ServicesActivated.objects.create(name=name, status=status,
                                                auth_required=auth_required,
                                                description=description)

    def test_servicesactivated(self):
        s = self.create_servicesactivated()
        self.assertTrue(isinstance(s, ServicesActivated))
        self.assertEqual(s.show(), "Service Activated %s %s %s %s" %
                         (s.name, s.status, s.auth_required, s.description))


class TriggerServiceTest(MainTest):

    """
        TriggerService Model
    """

    def test_triggerservice(self):
        t = self.create_triggerservice()
        self.assertTrue(isinstance(t, TriggerService))
        self.assertEqual(t.show(),
                         "My Service {} {} {} {}".format(t.user,
                                                         t.provider.name,
                                                         t.consumer.name,
                                                         t.description))
    """
        Form
    """

    def test_valid_form(self):
        t = self.create_triggerservice()
        data = {'description': t.description, }
        form = TriggerServiceForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        t = self.create_triggerservice()
        t.description = ''
        data = {'description': t.description, }
        form = TriggerServiceForm(data=data)
        self.assertFalse(form.is_valid())
