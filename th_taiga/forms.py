# coding: utf-8

from django import forms
from th_taiga.models import Taiga


class TaigaForm(forms.ModelForm):

    """
        form to handle Slack service
    """

    class Meta:
        model = Taiga
        fields = ('project_name', 'webhook_secret_key')


class TaigaProviderForm(TaigaForm):
    pass


class TaigaConsumerForm(TaigaForm):
    pass
