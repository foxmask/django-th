# -*- coding: utf-8 -*-
from django.db import models


class Services(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True
