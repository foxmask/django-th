# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Pushbullet(Services):

    """
        todoist model to be adapted for the new service
    """
    type = models.CharField(max_length=4, default='note')
    device = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    channel_tag = models.CharField(max_length=80, blank=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_pushbullet'

    def show(self):
        """

        :return: string representing object
        """
        return "My Pushbullet %s" % self.name

    def __str__(self):
        return "%s" % self.name
