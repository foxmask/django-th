# -*- coding: utf-8 -*-

from django import forms
from django_th.models.evernote import Evernote


class EvernoteForm(forms.ModelForm):

    """
        for to handle Evernote service
    """
    my_form_is = forms.CharField(widget=forms.HiddenInput(),
                                 initial='evernote')

    class Meta:
        model = Evernote
        fields = ('tag', 'notebook', 'my_form_is')
