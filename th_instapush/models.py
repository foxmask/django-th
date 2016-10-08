# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Instapush(Services):
    """

        wallabag model to be adapted for the new service
        to store url in your account

    """
    app_id = models.CharField(max_length=255)
    app_secret = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    tracker_name = models.CharField(max_length=80)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_instapush'

    def show(self):
        """

        string representing object
        """
        return "My Instapush %s" % self.name

    def __str__(self):
        return "%s" % self.name
