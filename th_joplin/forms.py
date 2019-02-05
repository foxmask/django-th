# coding: utf-8

from django import forms
from django.conf import settings
from django.forms import TextInput

from joplin_api import JoplinApi

from th_joplin.models import Joplin


class JoplinForm(forms.ModelForm):

    """
        for to handle Joplin service
    """

    folder = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        super(JoplinForm, self).__init__(*args, **kwargs)
        self.fields['folder'].choices = self.get_folders()

    def get_folders(self):
        """

        :return:
        """
        joplin = JoplinApi(token=settings.TH_JOPLIN_TOKEN)
        folders = joplin.get_folders().json()

        choices = []
        for folder in folders:
            line = (folder['id'], folder['title'])
            choices.append(line)
        return choices

    class Meta:
        model = Joplin
        fields = ('folder', )
        widgets = {
            'folder': TextInput(attrs={'class': 'form-control'}),
        }


class JoplinProviderForm(JoplinForm):
    pass


class JoplinConsumerForm(JoplinForm):
    pass
