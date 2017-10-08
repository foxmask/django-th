# coding: utf-8

from django import forms
from th_reddit.models import Reddit


class RedditForm(forms.ModelForm):

    """
        form to handle Reddit service
    """

    class Meta:
        model = Reddit
        fields = ['subreddit', 'share_link']


class RedditProviderForm(RedditForm):
    pass


class RedditConsumerForm(RedditForm):
    pass
