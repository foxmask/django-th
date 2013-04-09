# -*- coding: utf-8 -*-
from django.db import models
from .models.services import Services
# from .lib import *


class ServiceRSS(Services):

    class Meta(Services.Meta):
        db_table = 'rss'
