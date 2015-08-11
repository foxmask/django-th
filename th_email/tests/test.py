# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User
from th_email.models import Email
from django_th.models import TriggerService, UserService, ServicesActivated
from th_email.forms import EmailProviderForm, EmailConsumerForm


class EmailTest(TestCase):

    """
        EmailTest Model
    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20150808",
                              description="My first Service", status=True):
        user = self.user
        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceEmail', status=True,
            auth_required=True, description='Service Email')
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

    def create_email(self):
        trigger = self.create_triggerservice()
        email = 'foo@bar.com'
        status = True
        return Email.objects.create(trigger=trigger,
                                    email=email,
                                    status=status)

    def test_email(self):
        d = self.create_email()
        self.assertTrue(isinstance(d, Email))
        self.assertEqual(d.show(), "My Email %s" % (d.email))

    """
        Form
    """
    # provider
    def test_valid_provider_form(self):
        d = self.create_email()
        data = {'email': d.email}
        form = EmailProviderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_provider_form(self):
        form = EmailProviderForm(data={})
        self.assertFalse(form.is_valid())

    # consumer
    def test_valid_consumer_form(self):
        d = self.create_email()
        data = {'email': d.email}
        form = EmailConsumerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_consumer_form(self):
        form = EmailConsumerForm(data={})
        self.assertFalse(form.is_valid())
