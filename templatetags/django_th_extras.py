# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site
#from .models.rss import ServiceRss
#from .models.evernote import ServiceEvernote

register = template.Library()
current_site = Site.objects.get_current()


def th_details(input_str, trigger_id):
	from ..models.rss import ServiceRss
	from ..models.evernote import ServiceEvernote

	data = ServiceRss.objects.get(trigger_id=trigger_id)
	return data.url

register.filter(th_details)
