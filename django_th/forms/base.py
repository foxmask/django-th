from django import forms
from django.forms import TextInput, PasswordInput
from django.utils.translation import ugettext_lazy as _

# trigger happy
from django_th.models import User, UserService, \
    ServicesActivated, TriggerService


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
                   'date_created', 'status', 'result', 'date_result']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
        }


class UserServiceForm(forms.ModelForm):

    """
        Form to deal with my own activated service
    """

    def __init__(self, *args, **kwargs):
        super(UserServiceForm, self).__init__(*args, **kwargs)
        self.fields['token'] = forms.CharField(required=False)
        self.fields['name'].choices = activated_services(self.initial['user'])
        self.fields['name'].widget.attrs['class'] = 'form-control'

    def save(self, user=None):
        self.myobject = super(UserServiceForm, self).save(commit=False)
        self.myobject.user = user
        self.myobject.save()

    def clean(self):
        cleaned_data = super(UserServiceForm, self).clean()
        sa = ServicesActivated.objects.get(name=cleaned_data.get('name'))
        if sa.auth_required and sa.self_hosted:
            if cleaned_data.get('host') == '' or \
               cleaned_data.get('username') == '' or \
               cleaned_data.get('password') == '' or \
               cleaned_data.get('client_id') == '' or \
               cleaned_data.get('client_secret') == '':
                self.add_error(
                    'username', 'All the five fields are altogether mandatory')
            elif cleaned_data.get('host').endswith('/'):
                cleaned_data['host'] = cleaned_data['host'][:-1]

    class Meta:

        """
            meta to add/override anything we need
        """
        model = UserService
        exclude = ('user',)
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


def activated_services(user):
    """
        get the activated services added from the administrator
    """
    all_datas = ()
    data = ()
    services = ServicesActivated.objects.filter(status=1)
    for class_name in services:
        # only display the services that are not already used
        if UserService.objects.filter(name__exact=class_name.name,
                                      user__exact=user):
            continue
        # 2nd array position contains the name of the service
        else:
            data = (class_name.name,
                    class_name.name.rsplit('Service', 1)[1])
            all_datas = (data,) + all_datas
    return all_datas
