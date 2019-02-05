# coding: utf-8
from django.db import models
from django_th.models.services import Services
from django_th.models import TriggerService


class Joplin(Services):

    """
        joplin model to be adapted for the new service
    """
    folder = models.TextField()
    trigger = models.ForeignKey(TriggerService, on_delete=models.CASCADE)

    class Meta:
        app_label = 'th_joplin'
        db_table = 'django_th_joplin'

    def __str__(self):
        return self.name

    def show(self):
        return "My Joplin %s" % self.name
