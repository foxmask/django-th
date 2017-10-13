# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import caches
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, ListView, DeleteView
from django.db.models import Q
from django.utils.decorators import method_decorator

from django.urls import reverse, reverse_lazy

# trigger_happy
from django_th.models import TriggerService, UserService

from django_th.forms.base import TriggerServiceForm
from django_th.views_fbv import can_modify_trigger

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
cache = caches['django_th']

"""
   Part I : Triggers
"""


class TriggerListView(ListView):
    """
        list of Triggers
        the list can be filtered by service
    """
    context_object_name = "triggers_list"
    queryset = TriggerService.objects.all()
    template_name = "home.html"
    paginate_by = 3

    def get_paginate_by(self, queryset):
        """
            Get the number of items to paginate by,
            from the settings
        """
        return settings.DJANGO_TH.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        filtered_by = None
        # by default, sort by date_created
        ordered_by = (str('-date_triggered'), )
        # get the Trigger of the connected user
        if self.request.user.is_authenticated():
            # if the user selected a filter, get its ID
            if self.kwargs.get('trigger_filtered_by'):
                filtered_by = UserService.objects.filter(
                    user=self.request.user,
                    name=self.kwargs.get('trigger_filtered_by'))[0].id

            if self.kwargs.get('trigger_ordered_by'):
                """
                    sort by 'name' property in the related model UserService
                """
                order_by = str(self.kwargs.get('trigger_ordered_by') + "__name")
                # append to the tuple, the selected 'trigger_ordered_by'
                # choosen in the dropdown
                ordered_by = (order_by, ) + ordered_by

            # no filter selected
            if filtered_by is None:
                return self.queryset.filter(user=self.request.user).order_by(
                    *ordered_by).select_related('consumer__name',
                                                'provider__name')

            # filter selected : display all related triggers
            else:
                # here the queryset will do :
                # 1) get trigger of the connected user AND
                # 2) get the triggers where the provider OR the consumer match
                # the selected service
                return self.queryset.filter(user=self.request.user).filter(
                    Q(provider=filtered_by) |
                    Q(consumer=filtered_by)).order_by(
                    *ordered_by).select_related('consumer__name',
                                                'provider__name')
        # otherwise return nothing when user is not connected
        return TriggerService.objects.none()

    def get_context_data(self, **kwargs):
        """
            get the data of the view

            data are :
            1) number of triggers enabled
            2) number of triggers disabled
            3) number of activated services
            4) list of activated services by the connected user
        """
        triggers_enabled = triggers_disabled = services_activated = ()

        context = super(TriggerListView, self).get_context_data(**kwargs)

        if self.kwargs.get('trigger_filtered_by'):
            page_link = reverse('trigger_filter_by',
                                kwargs={'trigger_filtered_by':
                                        self.kwargs.get('trigger_filtered_by')})
        elif self.kwargs.get('trigger_ordered_by'):
            page_link = reverse('trigger_order_by',
                                kwargs={'trigger_ordered_by':
                                        self.kwargs.get('trigger_ordered_by')})
        else:
            page_link = reverse('home')

        if self.request.user.is_authenticated():
            # get the enabled triggers
            triggers_enabled = TriggerService.objects.filter(
                user=self.request.user, status=1).count()
            # get the disabled triggers
            triggers_disabled = TriggerService.objects.filter(
                user=self.request.user, status=0).count()
            # get the activated services
            user_service = UserService.objects.filter(user=self.request.user)
            """
                List of triggers activated by the user
            """
            context['trigger_filter_by'] = user_service
            """
                number of service activated for the current user
            """
            services_activated = user_service.count()

        """
            which triggers are enabled/disabled
        """
        context['nb_triggers'] = {'enabled': triggers_enabled,
                                  'disabled': triggers_disabled}
        """
            Number of services activated
        """
        context['nb_services'] = services_activated

        context['page_link'] = page_link
        context['fire'] = settings.DJANGO_TH.get('fire', False)

        return context


class TriggerServiceMixin(object):
    """
        Mixin for UpdateView and DeleteView
    """
    queryset = TriggerService.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerServiceMixin, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # get the trigger of the connected user
        if self.request.user.is_authenticated():
            return self.queryset.filter(user=self.request.user,
                                        id=self.kwargs.get('pk'))
        # otherwise return nothing
        return TriggerService.objects.none()


class TriggerUpdateView(TriggerServiceMixin, UpdateView):
    """
        Form to update description
    """
    form_class = TriggerServiceForm
    template_name = "triggers/edit_description_trigger.html"
    success_url = reverse_lazy("trigger_edit_thanks")

    def get_context_data(self, **kw):
        return super(TriggerUpdateView, self).get_context_data(**kw)

    def get(self, *args, **kwargs):
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        self.object = self.get_object()
        status = can_modify_trigger(self.request,
                                    self.object.provider.name.status,
                                    self.object.consumer.name.status)
        if status:
            return HttpResponseRedirect(reverse('base'))
        else:
            return super(TriggerUpdateView, self).get(
                self.request, *args, **kwargs)


class TriggerEditedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
    template_name = "triggers/edited_thanks_trigger.html"


class TriggerDeleteView(TriggerServiceMixin, DeleteView):
    """
        page to delete a trigger
    """
    template_name = "triggers/delete_trigger.html"
    success_url = reverse_lazy("trigger_delete_thanks")


class TriggerDeletedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
    template_name = "triggers/deleted_thanks_trigger.html"
