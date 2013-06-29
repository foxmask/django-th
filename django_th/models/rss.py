# -*- coding: utf-8 -*-
from django.db import models
from django_th.models.services import Services


class Rss(Services):

    url = models.URLField(max_length=255)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
