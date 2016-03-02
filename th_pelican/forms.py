# coding: utf-8

from django import forms
from django.forms import TextInput
from th_pelican.models import Pelican


class PelicanForm(forms.ModelForm):

    """
        for to handle Pelican service
    """

    class Meta:
        model = Pelican
        fields = ('title', 'url', 'category', 'tags', 'path')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
            'category': TextInput(attrs={'class': 'form-control'}),
            'tags': TextInput(attrs={'class': 'form-control'}),
            'path': TextInput(attrs={'class': 'form-control'}),
        }


class PelicanProviderForm(PelicanForm):
    pass


class PelicanConsumerForm(PelicanForm):
    pass
