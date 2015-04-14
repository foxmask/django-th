# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from django_th.models import UserProfile, TriggerService
from django_th.models import UserService, ServicesActivated
from django_th.forms.base import TriggerServiceForm
from django_th.forms.base import UserServiceForm


class UserProfileTest(TestCase):

    """
        UserProfile Model
    """
    def create_userprofile(self, user_id=111):
        return UserProfile.objects.create(user_id=user_id)

    def test_userprofile(self):
        u = self.create_userprofile()
        self.assertTrue(isinstance(u, UserProfile))
        self.assertEqual(u.show(), "User profile %s" % (u.user_id))


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
        self.assertEqual(u.show(), "User Service %s %s %s" %
                        (u.user, u.token, u.name))

    """
        Form - works with python 2.7.x - fails with python 3.4.0
    """
    def test_valid_form(self):
        u = self.create_userservice()
        if u.name.auth_required:
            data = {'user': u.user, 'name': u.name, 'token': u.token}
        else:
            data = {'user': u.user, 'name': u.name, 'token': ''}
        initial = {'user': self.user}
        form = UserServiceForm(data=data, initial=initial)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'user': '', 'name': '', 'token': ''}
        initial = {'user': self.user}
        form = UserServiceForm(data=data, initial=initial)
        self.assertFalse(form.is_valid())


class ServicesActivatedTest(TestCase):

    """
        ServicesActivated Model
    """
    def create_servicesactivated(self, name='ServiceRss', status=True,
                                 auth_required=False,
                                 description='RSS Feeds Service'):
        return ServicesActivated.objects.create(name=name, status=status,
                                                auth_required=auth_required,
                                                description=description)

    def test_servicesactivated(self):
        s = self.create_servicesactivated()
        self.assertTrue(isinstance(s, ServicesActivated))
        self.assertEqual(s.show(), "Service Activated %s %s %s %s" %
                         (s.name, s.status, s.auth_required, s.description))


class TriggerServiceTest(TestCase):

    """
        TriggerService Model
    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        user = self.user
        service_provider = ServicesActivated.objects.create(
            name='ServiceRss2', status=True,
            auth_required=False, description='Service RSS2')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceEvernote2', status=True,
            auth_required=True, description='Service Evernote2')
        provider = UserService.objects.create(user=user,
                                              token="",
                                              name=service_provider)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_consumer)
        return TriggerService.objects.create(provider=provider,
                                             consumer=consumer,
                                             user=user,
                                             date_created=date_created,
                                             description=description,
                                             status=status)

    def test_triggerservice(self):
        t = self.create_triggerservice()
        self.assertTrue(isinstance(t, TriggerService))
        self.assertEqual(t.show(), "My Service %s %s %s %s" %
                        (t.provider, t.consumer, t.description, t.user))

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
