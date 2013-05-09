# -*- coding: utf-8 -*-
from django.db import models
from ..models.services import Services


class ServiceRss(Services):

    url = models.URLField(max_length=255)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
