# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Holidays(models.Model):
    """
        get the trigger id and the current status of this one
        beware : we have to care about the actual status of
        of the trigger to avoid to activate one of them
        once we come back from Holidays, if it was disable
        before we activate Holidays mode
    """
    trigger = models.ForeignKey('TriggerService')
    user = models.ForeignKey(User)
    status = models.BooleanField()

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_holidays'

    def show(self):
        """

        :return: string representing object
        """
        return "Holidays for service %s" % self.trigger

    def __str__(self):
        return self.trigger
