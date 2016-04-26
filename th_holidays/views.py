# coding: utf-8
import arrow

from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from django_th.models import TriggerService
from th_holidays.models import Holidays
from th_holidays.forms import HolidaysForm


@login_required(login_url='login')
def holidays_done(request):
    """

        enable/disable the status of all MY triggers

    """
    template_name = "holidays/done.html"

    holidays = Holidays.objects.filter(user=request.user)
    if holidays.count() == 0:
        title = 'All your triggers are now all back online '
        title += 'like they were setup before you disabled them'
    else:
        title = 'All your triggers are now disable '
        title += 'until you come back here to enable them back'
    context = {'title': title}
    return render(request, template_name, {'context': context})


@login_required(login_url='login')
def holidays(request):
    """

        form to ask if I want to enable or
        disable MY triggers

    """
    template_name = 'holidays/activate.html'

    if request.method == 'GET':
        form = HolidaysForm()
        holidays = Holidays.objects.filter(user=request.user)
        if holidays.count() > 0:
            # holidays mode is on
            title = 'Are your sure you want to enable'
            title += ' all your triggers back now ?'
            description = ''
        else:
            # holidays mode is off
            title = 'Are your sure you want to activate this features now ?'
            description = 'Activating this feature will set off '
            description += 'all your triggers'
            description += ' until you come back here to disable the feature'
            description += ' to enable everything again'

        context = {'title': title, 'description': description}
    else:
        form = HolidaysForm(request.POST)
        if form.is_valid():
            holidays = Holidays.objects.filter(user=request.user)
            if holidays.count() > 0:
                now = arrow.utcnow().to(settings.TIME_ZONE).format(
                    'YYYY-MM-DD HH:mm:ss')
                # holidays mode is on
                for holiday in holidays:
                    trigger = TriggerService.objects.get(pk=holiday.trigger_id)
                    trigger.status = holiday.status
                    trigger.date_triggered = now
                    trigger.save()
                Holidays.objects.filter(user=request.user).delete()

            else:
                triggers = TriggerService.objects.filter(user=request.user)
                for trigger in triggers:
                    Holidays.objects.create(trigger=trigger,
                                            status=trigger.status,
                                            user=request.user)
                    trigger.status = False
                    trigger.save()

            return HttpResponseRedirect(reverse('holidays_done'))

    return render(request, template_name, {'form': form, 'context': context})
