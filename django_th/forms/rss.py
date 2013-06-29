# -*- coding: utf-8 -*-

from django import forms
from django_th.models.rss import Rss


class RssForm(forms.ModelForm):

    """
        for to handle Rss service
    """
    my_form_is = forms.CharField(widget=forms.HiddenInput(), initial='rss')

    class Meta:
        model = Rss
        fields = ('name', 'url', 'my_form_is')
