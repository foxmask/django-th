# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Taiga(Services):
    """
        Model for Taiga Service
    """
    project_name = models.CharField(max_length=50, blank=True)
    webhook_secret_key = models.CharField(max_length=50,
                                          blank=True,
                                          unique=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_taiga'

    def show(self):
        """

        :return: string representing object
        """
        return "Services Taiga %s" % self.trigger

    def __str__(self):
        return "%s" % self.trigger
