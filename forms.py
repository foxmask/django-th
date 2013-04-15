# -*- coding: utf-8 -*-
from django import forms
from django.forms import TextInput, PasswordInput
from django.utils.translation import ugettext as _
from .models import User, TriggerService, TriggerType, UserService, UserProfile
from .models.services import ServicesManaged
from .models.rss import ServiceRss
from .models.evernote import ServiceEvernote


def available_services():
    """
        get the activated services

        read the models dir to find the services installed
        to be added to the system by the administrator
    """
    import os
    models_services_dir = os.path.dirname(os.path.abspath(__file__))
    models_services_dir += '/models'
    all_datas = ()
    data = ()
    print models_services_dir
    for model_file in os.listdir(models_services_dir):
        if not model_file in ('services.py', 'services.pyc', \
                              '__init__.py', '__init__.pyc'):
            name, name_ext = model_file.rsplit('.', 1)
            if not name_ext == 'pyc':
                data = (name, name.capitalize())
                all_datas = (data,) + all_datas
    return all_datas


class TriggerTypeForm(forms.ModelForm):
    """
        TriggerType Form
    """
    class Meta:
        """
            meta to add/override anything we need
        """
        model = TriggerType
    name = forms.ModelChoiceField(queryset=TriggerType.objects.all())


class TriggerServiceForm(forms.ModelForm):
    """
        TriggerService Form
    """
    class Meta:
        """
            meta to add/override anything we need
        """
        model = TriggerService
        widgets = {
            'description':\
            TextInput(attrs={'placeholder':\
                             _('A description for your new service')}),
        }
        exclude = ('user',
                   'date_created')

    provider = forms.ModelChoiceField(queryset=TriggerType.objects.all())
    consummer = forms.ModelChoiceField(queryset=TriggerType.objects.all())

    def save(self, user=None):
        self.myobject = super(TriggerServiceForm, self).save(commit=False)
        self.myobject.user = user
        self.myobject.save()


class UserServiceForm(forms.ModelForm):
    """
        Form to deal with my own activated service
    """
    class Meta:
        """
            meta to add/override anything we need
        """
        model = UserService
        exclude = ('user',)

    code = forms.ModelChoiceField(queryset=TriggerType.objects.all())

    def save(self, user=None):
        self.myobject = super(UserServiceForm, self).save(commit=False)
        self.myobject.user = user
        self.myobject.save()


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


class ProfileForm(forms.ModelForm):
    """
        Form to manage the User profile
    """
    class Meta:
        """
        meta to override anything about UserProfile
        """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    email = forms.EmailField(label=_("Email"),
                             help_text=_('Your email will be used only in the \
                             following case and nothing more <ul><li>to send \
                             your activation mail</li><li>to send recovery \
                             password when you forgot yours</li><li>to send \
                             notifications</li></ul>'))
    last_name = forms.CharField(label=_('Last Name'))
    first_name = forms.CharField(label=_('First Name'))

    def save(self, commit=True):
        """
            Update the primary email address on the related User object as well
        """
        usr = self.instance.user
        usr.email = self.cleaned_data['email']
        usr.last_name = self.cleaned_data['last_name']
        usr.first_name = self.cleaned_data['first_name']
        usr.save()
        profile = super(ProfileForm, self).save(commit=False)
        return profile


class UserProfileForm(forms.ModelForm):
    """
        Form to deal with the fields of the User Model
    """
    first_name = forms.CharField(label=_('Last Name'), max_length=30)
    last_name = forms.CharField(label=_('First Name'), max_length=30)

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields.keyOrder = ['first_name', 'last_name', ]

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        """
            meta to override anything about UserProfile
        """
        model = UserProfile


class ServicesActivatedForm(forms.ModelForm):
    """
        get the list of the available services (the activated one)
    """
    class Meta:
        model = ServicesManaged
    """
        get the activated services
    """
    name = forms.ModelChoiceField(queryset=ServicesManaged.objects.all())


class ServicesManagedForm(forms.ModelForm):
    """
        get the list of the available services (the activated one)
    """
    class Meta:
        model = ServicesManaged

    status_values = (('0', 'Disabled'), (1, 'Enabled'), (2, 'Not installed'))
    status = forms.ChoiceField(status_values)
    name = forms.ChoiceField(available_services())


class EvernoteForm(forms.ModelForm):
    """
        for to handle Evernote service
    """
    class Meta:
        model = ServiceEvernote


class RssForm(forms.ModelForm):
    """
        for to handle Rss service
    """

    class Meta:
        model = ServiceRss

