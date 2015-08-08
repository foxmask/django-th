# coding: utf-8

from django import forms
from th_rss.models import Rss


class RssForm(forms.ModelForm):

    """
        form to handle Rss service
    """

    class Meta:
        model = Rss
        fields = ('name', 'url')


class RssProviderForm(RssForm):
    pass


class RssConsumerForm(RssForm):

    class Meta:
        model = Rss
        fields = ('name', )
