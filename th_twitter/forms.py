# coding: utf-8
from django import forms
from django.forms import TextInput
from th_twitter.models import Twitter


class TwitterForm(forms.ModelForm):

    """
        form to handle Twitter service
    """

    class Meta:
        model = Twitter
        fields = ('tag', 'screen')
        widgets = {
            'tag': TextInput(attrs={'class': 'form-control'}),
            'screen': TextInput(attrs={'class': 'form-control'}),
        }


class TwitterConsumerForm(TwitterForm):
    pass


class TwitterProviderForm(TwitterForm):
    pass
