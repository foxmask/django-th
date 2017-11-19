# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.utils.translation import ugettext as _

from th_twitter.models import Twitter


class TwitterForm(forms.ModelForm):

    """
        form to handle Twitter service
    """

    class Meta:
        model = Twitter
        fields = ['tag', 'screen', 'fav']

        widgets = {
            'tag': TextInput(attrs={'class': 'form-control'}),
            'screen': TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """
        validate if tag or screen is filled
        :return:
        """
        cleaned_data = super(TwitterForm, self).clean()
        tag = cleaned_data.get("tag")
        screen = cleaned_data.get("screen")
        # check if one of the field is filled when a field is empty the clean() function set it as None
        if tag is None and screen is None:
            raise ValidationError(_("You have to fill ONE of the fields (or tag + screen or screen + fav)"))


class TwitterConsumerForm(TwitterForm):
    pass


class TwitterProviderForm(TwitterForm):
    pass
