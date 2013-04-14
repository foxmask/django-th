# -*- coding: utf-8 -*-
from django.db import models


class Services(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % (self.name)


class ServicesManaged(Services):
    """
        service activated / desactivated from the admin
        to manage the service we want to give to the user
    """
    class Meta(Services.Meta):
        app_label = 'django_th'
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    status = models.IntegerField()

    def my_status(self):
        """
        customise the value of the status
        """
        if self.status == 1:
            my_status = 'Activated'
        elif self.status == 2:
            my_status = 'Offline'
        else:
            my_status = 'Not activated'
        return my_status
    my_status.admin_order_field = 'status'
    my_status.short_description = 'Status ?'
