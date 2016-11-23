# coding: utf-8

from django import forms
from th_slack.models import Slack


class SlackForm(forms.ModelForm):

    """
        form to handle Slack service
    """

    class Meta:
        model = Slack
        fields = ('webhook_url', )


class SlackProviderForm(SlackForm):
    pass


class SlackConsumerForm(SlackForm):
    pass
