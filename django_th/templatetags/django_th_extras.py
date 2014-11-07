# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='service_readable')
def service_readable(service):
    # service is a ServicesActivated object
    return service.name.rsplit('Service', 1)[1]
