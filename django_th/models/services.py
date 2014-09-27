# -*- coding: utf-8 -*-
from django.db import models


class Services(models.Model):
    """
        Main class for Services
    """
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.name)

    def show(self):
        return "Services Model %s %s %s " % (self.name, self.status, self.description)

    class Meta:
        app_label = 'django_th'
        abstract = True
        verbose_name = 'Services'
        verbose_name_plural = 'Services'
