# -*- coding: utf-8 -*-
from django.db import models
from services import ThServices


class ServiceEvernote(ThServices):

    tag = models.CharField(max_length=80)
    notebook = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    text = models.TextField()

    class Meta():
        app_label = 'django_th'
        verbose_name = 'Evernote'
        verbose_name_plural = 'Evernote'
