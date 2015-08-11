# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Email(Services):

    """
        Mail model to be adapted for the new service
    """
    email = models.EmailField()
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_email'

    def __str__(self):
        return "%s" % (self.email)

    def show(self):
        return "My Email %s" % (self.email)
