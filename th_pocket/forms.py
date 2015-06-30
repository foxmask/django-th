# coding: utf-8

from django import forms
from django.forms import TextInput
from th_pocket.models import Pocket


class PocketForm(forms.ModelForm):

    """
        for to handle Pocket service
    """

    class Meta:
        model = Pocket
        fields = ('tag',)
        widgets = {
            'tag': TextInput(attrs={'class': 'form-control'}),
        }


class PocketProviderForm(PocketForm):
    pass


class PocketConsumerForm(PocketForm):
    pass
