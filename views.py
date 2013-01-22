# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

# trigger_happy
from .models import TriggerService
from .forms import TriggerServiceForm, LoginForm, TriggerServiceDeleteForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def base(request):
    if request.user.is_authenticated():
        # logging
        logger.debug("base - user %s authenticated" % request.user.username)
        return home(request)
    else:
        # logging
        logger.debug("base - no user authenticated")

        template_name = 'base.html'
        login_form = LoginForm()
        context = {'form': login_form,
                   'user': request.user}
        context.update(csrf(request))
        return render_to_response(template_name,
                                  context,
                                  context_instance=RequestContext(request))


@login_required
def home(request):
    """
        the user's home
    """
    logger.debug("home - user %s authenticated" % request.user.username)
    template_name = 'home.html'
    datas = TriggerService.objects.filter(user_id__exact=request.user.id)\
                                            .order_by('-date_created')
    context = {'request': request,
                'user': request.user,
                'datas': datas}
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def add_service(request):
    """
        add a service
    """
    logger.debug("add_service - add a new service from authenticated user %s" % request.user.username)

    template_name = 'add_service.html'
    context = {'form': TriggerServiceForm(),
               'user': request.user,
               'action': 'add_service'}
    context.update(csrf(request))
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def edit_service(request, trigger_id):
    """
        edit a service
    """
    # TODO check the trigger_id content
    template_name = 'add_service.html'
    service = get_object_or_404(TriggerService, pk=trigger_id)
    form = TriggerServiceForm(instance=service)
    # 4) keep the data put in the form
    context = {'form': form,
               'trigger_id': trigger_id,
               'user': request.user,
               'action': 'edit_service'}
    context.update(csrf(request))
    # 5) go back to the form and display the values + errors
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def save_service(request):
    """
        save a service
    """
    if request.method == 'POST':  # If the form has been submitted...
        if request.POST['trigger_id'] != '':
            service = TriggerService.objects.get(pk=request.POST['trigger_id'])
            next_action = '/trigger/edited'
        else:
            service = TriggerService(user_id=request.user.id)
            next_action = '/trigger/added'
        form = TriggerServiceForm(request.POST, instance=service)
        # 1) valid the form
        if form.is_valid():  # All validation rules pass
            # logging
            logger.debug("'save_service' form is valid")
            form.save()
            logger.debug("'save_service' form saved")
            # 2) redirect user
            return HttpResponseRedirect(next_action)
            # return redirect('home')
        # 3) if not valid
        else:
            logger.error("'save_service' failed with method %s "\
                         % request.POST)
            template_name = 'add_service.html'
            # 4) keep the data put in the form
            context = {'form': form,
                       'user': request.user, }
            context.update(csrf(request))
            # 5) go back to the form and display the values + errors
            return render_to_response(template_name,
                                      context,
                                      context_instance=RequestContext(request))
    # attempt to acces to save_service by another method than POST
    else:
        # unbound form (if any)
        form = TriggerServiceForm()
    # redirect to home of the existing enabled services
    return redirect('home')


@login_required
def delete_service(request, trigger_id):
    """
        delete a service
    """
    # TODO check the trigger_id content
    template_name = 'delete_service.html'
    service = get_object_or_404(TriggerService, pk=trigger_id)
    form = TriggerServiceDeleteForm(instance=service)
    context = {'form': form,
               'service': service,
               'trigger_id': trigger_id,
               'user': request.user, }
    context.update(csrf(request))
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def deleted_service(request):
    """
        delete a service
    """
    print request.POST
    if 'ok' in request.POST:
        print request.POST['ok']
    if request.method == 'POST' and\
        'ok' in request.POST and\
        request.POST['trigger_id'] != '':  # If the form has been submitted...
        service = TriggerService.objects.get(pk=request.POST['trigger_id'])
        form = TriggerServiceDeleteForm(request.POST, instance=service)
        print form
        # 1) valid the form
        if form.is_valid():  # All validation rules pass
            # logging
            logger.debug("'deleted_service' form is valid")
            service.delete()
            logger.debug("'deleted_service' form deleted")
            # 2) redirect user
            return HttpResponseRedirect('/trigger/hasbeendeleted')
            # return redirect('home')
        # 3) if not valid
        else:
            logger.error("'deleted_service' failed with method %s "\
                         % request.POST)
            template_name = 'delete_service.html'
            # 4) keep the data put in the form
            context = {'form': form,
               'trigger_id': request.POST['trigger_id'],
               'user': request.user, }
            context.update(csrf(request))
            # 5) go back to the form and display the values + errors
            return render_to_response(template_name,
                                      context,
                                      context_instance=RequestContext(request))
    # attempt to acces to save_service by another method than POST
    else:
        # unbound form (if any)
        form = TriggerServiceForm()
    # redirect to home of the existing enabled services
    return redirect('home')


@login_required
def added_service(request):
    """
        display the added service page
    """

    context = {'sentance': 'Your service has been successfully created'}
    return render_to_response('thanks_service.html', context)


@login_required
def edited_service(request):
    """
        display the added service page
    """

    context = {'sentance': 'Your service has been successfully modified'}
    return render_to_response('thanks_service.html', context)


def hasbeendeleted_service(request):
    """
        display the deleted service page
    """
    context = {'sentance': 'Your service has been successfully deleted'}
    return render_to_response('thanks_service.html', context)


from django.contrib.auth import logout


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return redirect('base')
