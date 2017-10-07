# coding: utf-8

from django import forms
from django.forms import TextInput
from th_reddit.models import Reddit


class RedditForm(forms.ModelForm):

    """
        for to handle Reddit service
    """

    class Meta:
        model = Reddit
        fields = ('name',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }


class RedditProviderForm(RedditForm):
    pass


class RedditConsumerForm(RedditForm):
    pass
