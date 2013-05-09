# -*- coding: utf-8 -*-

from django import forms
from ..models.rss import ServiceRss


class RssForm(forms.ModelForm):
    """
        for to handle Rss service
    """
    my_form_is = forms.CharField(widget=forms.HiddenInput(), initial='rss')

    class Meta:
        model = ServiceRss
        fields = ('name', 'url', 'my_form_is')
