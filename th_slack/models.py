# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Slack(Services):
    """
        Model for Slack Service
    """
    webhook_url = models.URLField(max_length=2000, blank=True, null=True)
    slack_token = models.CharField(max_length=2000, blank=True, null=True)
    team_id = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_slack'

    def show(self):
        """

        :return: string representing object
        """
        return "Services Slack %s %s" % (self.trigger, self.webhook_url)

    def __str__(self):
        return "%s" % self.webhook_url
