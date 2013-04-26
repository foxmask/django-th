# -*- coding: utf-8 -*-

from django import forms
from ..models.evernote import ServiceEvernote


class EvernoteForm(forms.ModelForm):
    """
        for to handle Evernote service
    """
    my_form_is = forms.CharField(widget=forms.HiddenInput(),
                                 initial='evernote')

    class Meta:
        model = ServiceEvernote
        fields = ('tag', 'notebook', 'my_form_is')
