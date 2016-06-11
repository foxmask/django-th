# coding: utf-8

from django import forms

from django.forms import TextInput
from th_pushbullet.models import Pushbullet

PUSH_TYPE = (('note', 'Note'), ('link', 'Link'), ('file', 'File'))


class PushbulletForm(forms.ModelForm):

    """
        for to handle Todoist service
    """
    type = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Pushbullet
        fields = ('type', 'device', 'email', 'channel_tag')
        widgets = {
            'device': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'channel_tag': TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PushbulletForm, self).__init__(*args, **kwargs)
        self.fields['type'].choices = PUSH_TYPE


class PushbulletProviderForm(PushbulletForm):
    pass


class PushbulletConsumerForm(PushbulletForm):
    pass
