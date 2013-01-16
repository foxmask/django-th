# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.conf import settings


from django.contrib.auth.models import User

# trigger_happy
from django_th.models import TriggerHappy
from django_th.forms import TriggerHappyForm, LoginForm

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
    datas = TriggerHappy.objects.filter(user__username__exact=request.user.username).order_by('-date_created')
    context = {'request': request, 'datas': datas}
    return render_to_response(template_name,
                              context,
                              context_instance=RequestContext(request))


@login_required
def add_trigger(request):
    """
        add a trigger
    """
    pass


@login_required
def edit_trigger(request):
    """
        edit a trigger
    """
    pass


@login_required
def save_trigger(request):
    """
        save a trigger
    """
    pass


@login_required
def delete_trigger(request):
    """
        delete a trigger
    """
    pass


from django.contrib.auth import logout


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return redirect('base')
