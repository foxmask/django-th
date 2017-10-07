# coding: utf-8
from django.db import models
from django_th.models.services import Services
from django_th.models import TriggerService

"""
    https://dev.twitter.com/rest/public/timelines
    https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    https://dev.twitter.com/rest/reference/get/search/tweets

    Twitter model
    this permits to search tag or screen
    and store the last reached tweet_id with since_id, max_id, count
"""


class Twitter(Services):
    """

        Twitter model to store what the kind
        of data you want to handle

    """
    tag = models.CharField(max_length=80, null=True, blank=True)
    screen = models.CharField(max_length=80, null=True, blank=True)
    fav = models.BooleanField(default=False)
    since_id = models.BigIntegerField(null=True, blank=True)
    max_id = models.BigIntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    trigger = models.ForeignKey(TriggerService)

    class Meta:
        app_label = 'th_twitter'
        db_table = 'django_th_twitter'

    def show(self):
        """

        :return: string representing object
        """
        return "My Twitter %s %s %s" % (self.screen, self.tag, self.fav)

    def __str__(self):
        return "%s" % self.screen
