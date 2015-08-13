# coding: utf-8

from django import forms
from django.forms import TextInput
from th_trello.models import Trello


class TrelloForm(forms.ModelForm):

    """
        for to handle Trello service
    """

    class Meta:
        model = Trello
        fields = ('board_name', 'list_name')
        widgets = {
            'board_name': TextInput(attrs={'class': 'form-control'}),
            'list_name': TextInput(attrs={'class': 'form-control'}),
        }


class TrelloProviderForm(TrelloForm):
    pass


class TrelloConsumerForm(TrelloForm):
    pass
