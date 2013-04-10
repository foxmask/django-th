# -*- coding: utf-8 -*-
from django.db import models
from services import Services


class ServiceRss(Services):

    class Meta(Services.Meta):
        db_table = 'rss'
