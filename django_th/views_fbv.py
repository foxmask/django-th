# coding: utf-8
from __future__ import unicode_literals
import arrow
# django
from django.core.cache import caches
from django.core import management
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
# django_th
from django_th.tools import get_service
from django_th.models import TriggerService, ServicesActivated

cache = caches['django_th']


def can_modify_trigger(request, provider, consumer):
    # do not permit to edit the details of one trigger
    # if the provider or consumer is disabled
    if provider and consumer:
        return False
    else:
        from django.contrib import messages
        messages.warning(request, 'You cant modify a disabled trigger')
        return True


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return HttpResponseRedirect(reverse('base'))


def trigger_on_off(request, trigger_id):
    """
        enable/disable the status of the trigger then go back home
        :param request: request object
        :param trigger_id: the trigger ID to switch the status to True or False
        :type request: HttpRequest object
        :type trigger_id: int
        :return render
        :rtype HttpResponse
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format(
        'YYYY-MM-DD HH:mm:ssZZ')
    trigger = get_object_or_404(TriggerService, pk=trigger_id)
    if trigger.status:
        title = 'disabled'
        title_trigger = _('Set this trigger on')
        btn = 'success'
        trigger.status = False
    else:
        title = _('Edit your service')
        title_trigger = _('Set this trigger off')
        btn = 'primary'
        trigger.status = True
        # set the trigger to the current date when the
        # the trigger is back online
        trigger.date_triggered = now
    trigger.save()

    return render(request, 'triggers/trigger_line.html',
                           {'trigger': trigger,
                            'title': title,
                            'title_trigger': title_trigger,
                            'btn': btn})


def fire_trigger(request, trigger_id):
    """
        start the handling of only ONE trigger
        :param request: request object
        :param trigger_id: the trigger ID to switch the status to True or False
        :type request: HttpRequest object
        :type trigger_id: int
        :return render
        :rtype HttpResponse
    """
    date = ''

    if cache.get('django_th' + '_fire_trigger_' + str(trigger_id)):
        template = 'triggers/fire_trigger_ko.html'
        trigger = TriggerService.objects.get(id=trigger_id)
        kwargs = {'trigger': trigger}
    else:
        now = arrow.utcnow().to(settings.TIME_ZONE).format(
            'YYYY-MM-DD HH:mm:ssZZ')

        cache.set('django_th' + '_fire_trigger_' + str(trigger_id), '*')
        management.call_command('read_n_pub', trigger_id=trigger_id)

        trigger = TriggerService.objects.get(id=trigger_id)
        date_result = arrow.get(trigger.date_result).to(settings.TIME_ZONE)\
            .format('YYYY-MM-DD HH:mm:ssZZ')
        date_triggered = arrow.get(trigger.date_triggered).\
            to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')

        if date_result < date_triggered and date_triggered > now:
            date = '*'

        template = 'triggers/fire_trigger.html'
        kwargs = {'trigger': trigger, 'date': date}

    return render(request, template, kwargs)


def service_related_triggers_switch_to(request, user_service_id, switch):
    """
        switch the status of all the triggers related to the service,
        then go back home
        :param request: request object
        :param user_service_id: the service ID to switch the status to
        True or False of all the related trigger
        :param switch: the switch value
        :type request: HttpRequest object
        :type user_service_id: int
        :type switch: string off or on
    """
    status = True
    if switch == 'off':
        status = False

    TriggerService.objects.filter(provider__id=user_service_id).update(
        status=status)
    TriggerService.objects.filter(consumer__id=user_service_id).update(
        status=status)

    return HttpResponseRedirect(reverse('user_services'))


def trigger_switch_all_to(request, switch):
    """
        switch the status of all the "my" triggers then go back home
        :param request: request object
        :param switch: the switch value
        :type request: HttpRequest object
        :type switch: string off or on
    """
    now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ss')
    status = True
    if switch == 'off':
        status = False
    if status:
        TriggerService.objects.filter(user=request.user).update(
            status=status, date_triggered=now)
    else:
        TriggerService.objects.filter(user=request.user).update(status=status)

    return HttpResponseRedirect(reverse('base'))


def list_services(request, step):
    """
        get the activated services added from the administrator
        :param request: request object
        :param step: the step which is proceeded
        :type request: HttpRequest object
        :type step: string
        :return the activated services added from the administrator
    """
    all_datas = []

    if step == '0':
        services = ServicesActivated.objects.filter(status=1)
    elif step == '3':
        services = ServicesActivated.objects.filter(status=1,
                                                    id__iexact=request.id)
    for class_name in services:
        all_datas.append({class_name: class_name.name.rsplit('Service', 1)[1]})

    return all_datas


def trigger_edit(request, trigger_id, edit_what):
    """
        edit the provider
        :param request: request object
        :param trigger_id: ID of the trigger to edit
        :param edit_what: edit a 'Provider' or 'Consumer' ?
        :type request: HttpRequest object
        :type trigger_id: int
        :type edit_what: string
        :return render
        :rtype HttpResponse
    """
    if edit_what not in ('Provider', 'Consumer'):
        # bad request
        return redirect('base')

    form_name = edit_what + 'Form'

    # get the trigger object
    service = TriggerService.objects.get(id=trigger_id)

    if can_modify_trigger(request,
                          service.provider.name.status,
                          service.consumer.name.status):
        return HttpResponseRedirect(reverse('base'))

    if edit_what == 'Consumer':
        my_service = service.consumer.name.name
    else:
        my_service = service.provider.name.name

    # get the service name
    service_name = str(my_service).split('Service')[1]
    # get the model of this service
    model = get_service(my_service)

    # get the data of this service linked to that trigger
    data = model.objects.get(trigger_id=trigger_id)

    template = service_name.lower() + '/edit_' + edit_what.lower() + ".html"

    if request.method == 'POST':
        form = get_service(my_service, 'forms', form_name)(
            request.POST, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('trigger_edit_thanks'))
    else:
        form = get_service(my_service, 'forms', form_name)(instance=data)

    context = {'description': service.description, 'edit_what': edit_what}
    return render(request, template, {'form': form, 'context': context})
