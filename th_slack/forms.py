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

    class Meta:
        model = Slack
        fields = ('team_id', 'slack_token', 'channel')


class SlackConsumerForm(SlackForm):

    class Meta:
        model = Slack
        fields = ('webhook_url', )
