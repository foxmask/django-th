# -*- coding: utf-8 -*-

from django import forms
from ..models.evernote import ServiceEvernote


class EvernoteForm(forms.ModelForm):
    """
        for to handle Evernote service
    """
    class Meta:
        model = ServiceEvernote
        fields = ('tag', 'notebook')
