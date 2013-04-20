# -*- coding: utf-8 -*-

from django import forms
from ..models.rss import ServiceRss


class RssForm(forms.ModelForm):
    """
        for to handle Rss service
    """
    class Meta:
        model = ServiceRss
        fields = ('name', 'url')
