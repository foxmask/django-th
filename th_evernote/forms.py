# coding: utf-8

from django import forms
from django.forms import TextInput
from th_evernote.models import Evernote


class EvernoteForm(forms.ModelForm):

    """
        for to handle Evernote service
    """

    class Meta:
        model = Evernote
        fields = ('tag', 'notebook', )
        widgets = {
            'tag': TextInput(attrs={'class': 'form-control'}),
            'notebook': TextInput(attrs={'class': 'form-control'}),
        }


class EvernoteConsumerForm(EvernoteForm):
    pass


class EvernoteProviderForm(EvernoteForm):
    pass
