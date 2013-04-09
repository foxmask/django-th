# -*- coding: utf-8 -*-
from django.db import models
from .models.services import Services
# from .lib import *


class ServiceEvernote(Services):

    tag = models.CharField(max_length=80)
    notebook = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    text = models.TextField()

    class Meta(Services.Meta):
        db_table = 'evernote'
