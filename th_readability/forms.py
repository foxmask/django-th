# coding: utf-8

from django import forms
from django.forms import TextInput
from th_readability.models import Readability


class ReadabilityForm(forms.ModelForm):

    """
        for to handle Readability service
    """

    class Meta:
        model = Readability
        fields = ('tag',)
        widgets = {
            'tag': TextInput(attrs={'class': 'form-control'}),
        }


class ReadabilityProviderForm(ReadabilityForm):
    pass


class ReadabilityConsumerForm(ReadabilityForm):
    pass
