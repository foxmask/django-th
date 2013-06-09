# -*- coding: utf-8 -*-
from django.db import models
from ..models.services import Services


class Evernote(Services):

    tag = models.CharField(max_length=80, blank=True)
    notebook = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    text = models.TextField()
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
