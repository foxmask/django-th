# coding: utf-8
from django.db import models
from django_th.models.services import Services
from django_th.models import TriggerService


class Reddit(Services):

    """
        reddit model to be adapted for the new service
    """
    # put whatever you need  here
    # eg title = models.CharField(max_length=80)
    # but keep at least this one
    subreddit = models.CharField(max_length=80)
    share_link = models.BooleanField(default=False)
    trigger = models.ForeignKey(TriggerService)

    class Meta:
        app_label = 'th_reddit'
        db_table = 'django_th_reddit'

    def __str__(self):
        return self.subreddit

    def show(self):
        return "My Reddit %s" % self.subreddit
