# coding: utf-8

from django import forms
from django.forms import TextInput
from th_tumblr.models import Tumblr


class TumblrForm(forms.ModelForm):

    """
        for to handle Tumblr service
    """

    class Meta:
        model = Tumblr
        fields = ('blogname', 'tag')
        widgets = {
            'blogname': TextInput(attrs={'class': 'form-control'}),
            'tag': TextInput(attrs={'class': 'form-control'}),
        }


class TumblrProviderForm(TumblrForm):
    pass


class TumblrConsumerForm(TumblrForm):
    pass
