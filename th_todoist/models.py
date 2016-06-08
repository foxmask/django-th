# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Todoist(Services):

    """
        todoist model to be adapted for the new service
    """
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_todoist'

    def __str__(self):
        return self.name

    def show(self):
        return "My Todoist %s" % self.name
