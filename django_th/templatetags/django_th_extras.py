# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site

register = template.Library()
current_site = Site.objects.get_current()
