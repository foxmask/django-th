# coding: utf-8
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_joplin.models import Joplin
from django_th.models import TriggerService, UserService, ServicesActivated
# from th_joplin.forms import JoplinProviderForm, JoplinConsumerForm


class JoplinTest(TestCase):

    """
        joplinTest Model
    """
    def setUp(self):
        """
           create a user
        """
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        """
           create a TriggerService
        """
        user = self.user

        service_provider = ServicesActivated.objects.create(
            name='ServiceRSS', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServiceJoplin', status=True,
            auth_required=True, description='Service Joplin')
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

    def create_joplin(self):
        """
            Create a Joplin object related to the trigger object
        """
        trigger = self.create_triggerservice()
        name = 'joplin'
        status = True
        return Joplin.objects.create(trigger=trigger, name=name, folder="test", status=status)

    def test_joplin(self):
        """
           Test if the creation of the joplin object looks fine
        """
        d = self.create_joplin()
        self.assertTrue(isinstance(d, Joplin))
        self.assertEqual(d.show(), "My Joplin %s" % d.name)

    """
        Form
    """
    # provider
    # def test_valid_provider_form(self):
    #    """
    #       test if that form is a valid provider one
    #    """
    #    d = self.create_joplin()
    #    data = {'folder': d.folder}
    #    form = JoplinProviderForm(data=data)
    #    self.assertTrue(form.is_valid())

    # def test_invalid_provider_form(self):
    #    """
    #       test if that form is not a valid provider one
    #    """
    #    form = JoplinProviderForm(data={})
    #    self.assertFalse(form.is_valid())

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_JOPLIN_WEBCLIPPER)
        self.assertTrue(settings.TH_JOPLIN_TOKEN)
