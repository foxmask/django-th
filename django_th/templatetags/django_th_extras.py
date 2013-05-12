# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site

register = template.Library()
current_site = Site.objects.get_current()


@register.filter(name='service_readable')
def service_readable(service):
    # service is a ServicesActivated object
    return service.name.rsplit('Service', 1)[1]
