# coding: utf-8

from django import forms
from django.forms import TextInput
from th_github.models import Github


class GithubForm(forms.ModelForm):

    """
        for to handle Pocket service
    """

    class Meta:
        model = Github
        fields = ('repo', 'project')
        widgets = {
            'repo': TextInput(attrs={'class': 'form-control'}),
            'project': TextInput(attrs={'class': 'form-control'}),
        }


class GithubProviderForm(GithubForm):
    pass


class GithubConsumerForm(GithubForm):
    pass
