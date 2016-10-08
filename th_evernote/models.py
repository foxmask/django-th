# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Evernote(Services):
    """

        Evernote model to store all notes

    """
    tag = models.CharField(max_length=80, blank=True)
    notebook = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    text = models.TextField()
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_evernote'

    def show(self):
        """

        :return: string representing object
        """
        return "My Evernote %s" % self.title

    def __str__(self):
        return "%s" % self.title
