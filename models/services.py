# -*- coding: utf-8 -*-
from django.db import models


class Services(models.Model):
    """
        Main class for Services
    """
    name = models.CharField(max_length=255, unique=True)
    status = models.BooleanField()
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        app_label = 'django_th'
        abstract = True
        verbose_name = 'Services'
        verbose_name_plural = 'Services'
