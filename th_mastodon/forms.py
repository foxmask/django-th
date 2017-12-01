# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.utils.translation import ugettext as _
from th_mastodon.models import Mastodon


class MastodonForm(forms.ModelForm):

    """
        form to handle Mastodon service
    """

    class Meta:
        model = Mastodon
        fields = ['timeline', 'tooter', 'tag', 'fav']

        widgets = {
            'tag': TextInput(attrs={'class': 'form-control'}),
            'tooter': TextInput(attrs={'placeholder': '@username@mastodo.tld',
                                       'class': 'form-control'}),
        }

    def clean(self):
        """
        validate if tag or screen is filled
        :return:
        """
        cleaned_data = super(MastodonForm, self).clean()
        tag = cleaned_data.get("tag")
        screen = cleaned_data.get("tooter")
        # check if one of the field is filled when a field is empty the clean() function set it as None
        if tag is None and screen is None:
            raise ValidationError(_("You have to fill ONE of the fields (or tag + tooter or tooter + fav)"))


class MastodonProviderForm(MastodonForm):
    pass


class MastodonConsumerForm(MastodonForm):
    pass
