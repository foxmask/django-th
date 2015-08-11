# coding: utf-8

from django import forms
from django.forms import TextInput
from th_email.models import Email


class EmailForm(forms.ModelForm):

    """
        for to handle Pocket service
    """

    class Meta:
        model = Email
        fields = ('email',)
        widgets = {
            'email': TextInput(attrs={'class': 'form-control'}),
        }


class EmailProviderForm(EmailForm):
    pass


class EmailConsumerForm(EmailForm):
    pass
