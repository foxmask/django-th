# coding: utf-8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_th.models.services import Services


@python_2_unicode_compatible
class Readability(Services):
    """

        Readability model to store how you want
        to store url in your account

    """
    tag = models.CharField(max_length=80, blank=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_readability'

    def __str__(self):
        return self.name

    def show(self):
        return "My Readability %s" % self.name
