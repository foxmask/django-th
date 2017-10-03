# coding: utf-8
from django.db import models
from django_th.models.services import Services
from django_th.models import TriggerService


class Tumblr(Services):

    """
        tumblr model to be adapted for the new service
    """
    blogname = models.CharField(max_length=80)
    tag = models.CharField(max_length=80, blank=True)
    trigger = models.ForeignKey(TriggerService)

    class Meta:
        app_label = 'th_tumblr'
        db_table = 'django_th_tumblr'

    def __str__(self):
        return self.blogname

    def show(self):
        return "My Tumblr %s" % self.blogname
