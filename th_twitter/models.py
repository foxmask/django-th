# coding: utf-8
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django_th.models.services import Services

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
    since_id = models.BigIntegerField(null=True, blank=True)
    max_id = models.BigIntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_twitter'

    def clean(self):
        """
        validate if tag or screen is filled
        :return:
        """
        # check if one of the field is filled
        if self.tag == '' and self.screen == '':
            raise ValidationError(
                _("You have to fill ONE of the both fields (or all together)"))

    def show(self):
        """

        :return: string representing object
        """
        return "My Twitter %s %s" % (self.screen, self.tag)

    def __str__(self):
        return "%s" % self.screen
