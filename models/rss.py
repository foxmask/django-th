# -*- coding: utf-8 -*-
from django.db import models
from ..models.services import ServicesMgr


class ServiceRss(ServicesMgr):

    url = models.URLField(max_length=255)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        verbose_name = 'RSS'
        verbose_name_plural = 'RSS'
