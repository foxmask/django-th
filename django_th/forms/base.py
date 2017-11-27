# coding: utf-8
from django import forms
from django.forms import TextInput, PasswordInput
from django.utils.translation import ugettext_lazy as _

# trigger happy
from django_th.models import User, UserService, ServicesActivated, TriggerService


class TriggerServiceForm(forms.ModelForm):

    """
        Form to edit the description
    """
    class Meta:

        """
            meta to add/override anything we need
        """
        model = TriggerService
        exclude = ['provider', 'consumer', 'user', 'date_triggered',
                   'date_created', 'status', 'result', 'date_result',
                   'consumer_failed', 'provider_failed', 'counter_ok',
                   'counter_ko']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
        }


class UserServiceForm(forms.ModelForm):

    """
        Form to deal with my own activated service
    """
    def save(self, user=None, service_name=''):
        """

        :param user:
        :param service_name:
        :return:
        """
        self.myobject = super(UserServiceForm, self).save(commit=False)
        self.myobject.user = user
        self.myobject.name = ServicesActivated.objects.get(name=self.initial['name'])
        self.myobject.save()

    def clean(self):
        """
        check the content of each field
        :return:
        """
        cleaned_data = super(UserServiceForm, self).clean()
        sa = ServicesActivated.objects.get(name=self.initial['name'])
        # set the name of the service, related to ServicesActivated model
        cleaned_data['name'] = sa
        if sa.auth_required and sa.self_hosted:
            if cleaned_data.get('host') == '' or \
               cleaned_data.get('username') == '' or \
               cleaned_data.get('password') == '' or \
               cleaned_data.get('client_id') == '' or \
               cleaned_data.get('client_secret') == '':
                self.add_error('username', 'All the five fields are altogether mandatory')
            elif cleaned_data.get('host') is None:
                self.add_error('host', 'Check its protocol and its name')
            elif cleaned_data.get('host').endswith('/'):
                cleaned_data['host'] = cleaned_data['host'][:-1]

    class Meta:

        """
            meta to add/override anything we need
        """
        model = UserService
        exclude = ('name', 'user', 'counter_ok', 'counter_ko')
        widgets = {
            'host': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'client_id': TextInput(attrs={'class': 'form-control'}),
            'client_secret': TextInput(attrs={'class': 'form-control'}),
            'token': TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.ModelForm):

    """
        Form to manage the login page
    """
    class Meta:
        model = User
        widgets = {
            'username': TextInput(attrs={'placeholder': _('Username')}),
            'password': PasswordInput(attrs={'placeholder': _('Password')}),
        }
        exclude = ()
