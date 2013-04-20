# -*- coding: utf-8 -*-
from django.db import models
from services import ThServices


class ServiceRss(ThServices):

    url = models.URLField(max_length=255)

    class Meta():
        app_label = 'django_th'
        verbose_name = 'RSS'
        verbose_name_plural = 'RSS'
