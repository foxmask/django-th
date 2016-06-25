# coding: utf-8

from django import forms
from django.forms import TextInput
from th_instapush.models import Instapush


class InstapushForm(forms.ModelForm):

    """
        for to handle Wallabag service
    """

    class Meta:
        model = Instapush
        fields = ('app_id',
                  'app_secret',
                  'event_name',
                  'tracker_name')
        widgets = {
            'app_id': TextInput(attrs={'class': 'form-control'}),
            'app_secret': TextInput(attrs={'class': 'form-control'}),
            'event_name': TextInput(attrs={'class': 'form-control'}),
            'tracker_name': TextInput(attrs={'class': 'form-control'}),
        }


class InstapushProviderForm(InstapushForm):
    pass


class InstapushConsumerForm(InstapushForm):
    pass
