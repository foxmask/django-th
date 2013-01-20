# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

# trigger_happy
from .models import TriggerService
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


#  @login_required
def edit_service(request):
    """
        edit a service
    """
    print request.id
    # service = TriggerService(user_id=request.user.id)
    template_name = 'add_service.html'
    form = TriggerServiceForm(request.id)
    # 4) keep the data put in the form
    context = {'form': form,
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
        service = TriggerService(user_id=request.user.id)
        form = TriggerServiceForm(request.POST, instance=service)
        # 1) valid the form
        if form.is_valid():  # All validation rules pass
            # logging
            logger.debug("'save_service' form is valid")
            form.save()
            logger.debug("'save_service' form saved")
            # 2) redirect user
            return HttpResponseRedirect('/trigger/added')
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
def delete_service(request):
    """
        delete a service
    """
    pass


@login_required
def added_service(request):
    """
        display the added service page
    """
    return render_to_response('added_service.html')


from django.contrib.auth import logout


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return redirect('base')
