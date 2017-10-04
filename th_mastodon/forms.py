# coding: utf-8

from django import forms
from th_mastodon.models import Mastodon


class MastodonForm(forms.ModelForm):

    """
        form to handle Mastodon service
    """

    class Meta:
        model = Mastodon
        fields = ['timeline', 'tooter', 'tag', 'fav']


class MastodonProviderForm(MastodonForm):
    pass


class MastodonConsumerForm(MastodonForm):
    pass
