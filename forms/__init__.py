# -*- coding: utf-8 -*-
from django import forms
from django.forms import TextInput, PasswordInput
from django.utils.translation import ugettext as _
from ..models import User, TriggerService, UserService, UserProfile
from ..models import ServicesActivated


class UserServiceForm(forms.ModelForm):
    """
        Form to deal with my own activated service
    """
    def save(self, user=None):
        self.myobject = super(UserServiceForm, self).save(commit=False)
        self.myobject.user = user
        self.myobject.save()

    def __init__(self, *args, **kwargs):
        super(UserServiceForm, self).__init__(*args, **kwargs)
        self.fields['name'].initial = forms.ModelChoiceField(
            queryset=ServicesActivated.objects.filter(status=1))

    class Meta:
        """
            meta to add/override anything we need
        """
        model = UserService
        exclude = ('user',)


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
            'description':
            TextInput(attrs={'placeholder':
                             _('A description for your new service')}),
        }
        exclude = ('user',
                   'date_created')

    provider = forms.ModelChoiceField(queryset=UserService.objects.all())
    consummer = forms.ModelChoiceField(queryset=UserService.objects.all())

    def save(self, user=None):
        self.myobject = super(TriggerServiceForm, self).save(commit=False)
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


class ServicesDescriptionForm(forms.ModelForm):
    my_form_is = forms.CharField(
        widget=forms.HiddenInput(),
        initial='description')

    class Meta:
        model = TriggerService
        widgets = {'description':
                   TextInput(attrs={'placeholder':
                                    _('A description for your new service')}),
                   }
        fields = ('description', 'my_form_is', )
