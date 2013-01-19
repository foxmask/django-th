# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

# trigger_happy
from .models import TriggerService, TriggerType
from .forms import TriggerServiceForm, LoginForm

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
                   'user': request.user,
                   'username': request.user.username}
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
    datas = TriggerService.objects.filter(user__username__exact=request.user.username).order_by('-date_created')
    context = {'request': request, 'datas': datas}
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def add_service(request):
    """
        add a service
    """
    logger.debug("add a new serviceno user authenticated")

    template_name = 'add_service.html'
    context = {'form': TriggerServiceForm(),
               'user': request.user, }
    context.update(csrf(request))
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def edit_service(request):
    """
        edit a service
    """
    pass


@login_required
def save_service(request):
    """
        save a service
    """
    if request.method == 'POST':  # If the form has been submitted...
        service = TriggerService(user_id=request.user.id)
        form = TriggerServiceForm(request.POST, instance=service)
        # 1) valid the form
        if form.is_valid():  # All validation rules pass
            # logging
            logger.debug("'save_service' form is valid")
            form.save()
            service_provider = TriggerType(code=form.cleaned_data['provider'])
            service_consummer = TriggerType(code=form.cleaned_data['consummer'])
            service_provider.triggerservice.add(service)
            service_consummer.triggerservice.add(service)

            logger.debug("'save_service' form saved")
            return redirect('home')
    else:
        # logging
        logger.error("'save_service' failed with method %s " % request.POST)
        form = TriggerServiceForm()  # An unbound form

    return render_to_response('home.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def delete_service(request):
    """
        delete a service
    """
    pass


from django.contrib.auth import logout


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return redirect('base')
