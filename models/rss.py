# -*- coding: utf-8 -*-
from django.db import models
from services import Services


class ServiceRss(Services):

    url = models.URLField(max_length=255)

    class Meta(Services.Meta):
        app_label = 'django_th'
        verbose_name = 'RSS'
        verbose_name_plural = 'RSS'
