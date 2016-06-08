# coding: utf-8

from django import forms

from th_todoist.models import Todoist


class TodoistForm(forms.ModelForm):

    """
        for to handle Todoist service
    """

    class Meta:
        model = Todoist
        fields = ()


class TodoistProviderForm(TodoistForm):
    pass


class TodoistConsumerForm(TodoistForm):
    pass
