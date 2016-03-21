# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='service_readable')
def service_readable(service):
    # service is a ServicesActivated object
    return service.name.rsplit('Service', 1)[1]


@register.filter(name='trigger_disabled')
def trigger_disabled(trigger):
    if trigger.provider.name.status is False:
        return 'trigger-disable'
    if trigger.consumer.name.status is False:
        return 'trigger-disable'
