# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
# from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, UpdateView, \
    DeleteView, ListView, TemplateView

from django.contrib.formtools.wizard.views import SessionWizardView

# trigger_happy
from .models import TriggerService, UserService
from .models.services import ThServices
from .forms import TriggerServiceForm, UserServiceForm
from .service_provider import service_provider

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

service_provider.load_services()

from django.contrib.auth import logout


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return redirect('base')


#*************************************
#  Part I : the Triggers
#*************************************


class TriggerListView(ListView):
    context_object_name = "triggers_list"
    queryset = TriggerService.objects.all()
    template_name = "home.html"

    def get_queryset(self):
        # get the Trigger of the connected user
        if self.request.user.is_authenticated():
            return self.queryset.filter(user=self.request.user).\
                                        order_by('-date_created')
        # otherwise return nothing
        return TriggerService.objects.none()


class TriggerCreateView(CreateView):
    form_class = TriggerServiceForm
    template_name = "triggers/add_trigger.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return HttpResponseRedirect('/trigger/add/thanks/')

    def get_context_data(self, **kw):
        context = super(TriggerCreateView, self).get_context_data(**kw)
        context['action'] = 'add_trigger'
        return context


class TriggerUpdateView(UpdateView):
    form_class = TriggerServiceForm
    template_name = "triggers/add_trigger.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kw):
        return super(TriggerUpdateView, self).dispatch(*args, **kw)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return HttpResponseRedirect('/trigger/edit/thanks/')

    def get_object(self, queryset=None):
        obj = TriggerService.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kw):
        context = super(TriggerUpdateView, self).get_context_data(**kw)
        context['action'] = 'edit_trigger'
        return context


class TriggerDeleteView(DeleteView):
    queryset = TriggerService.objects.all()
    template_name = "triggers/delete_trigger.html"
    success_url = '/trigger/delete/thanks/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerDeleteView, self).dispatch(*args, **kwargs)


class TriggerAddedTemplateView(TemplateView):
    template_name = "triggers/thanks_trigger.html"

    def get_context_data(self, **kw):
        context = super(TriggerAddedTemplateView, self).get_context_data(**kw)
        context['sentance'] = 'Your trigger has been successfully created'
        return context


class TriggerEditedTemplateView(TemplateView):
    template_name = "triggers/thanks_trigger.html"

    def get_context_data(self, **kw):
        context = super(TriggerEditedTemplateView, self).get_context_data(**kw)
        context['sentance'] = 'Your trigger has been successfully modified'
        return context


class TriggerDeletedTemplateView(TemplateView):
    template_name = "triggers/thanks_trigger.html"

    def get_context_data(self, **kw):
        context = super(TriggerDeletedTemplateView, self).\
                                                        get_context_data(**kw)
        context['sentance'] = 'Your trigger has been successfully deleted'
        return context


#*************************************
#  Part II : the UserServices
#*************************************


class UserServiceListView(ListView):
    context_object_name = "services_list"
    queryset = UserService.objects.all()
    template_name = "services/services.html"

    def get_queryset(self):
        # get the Service of the connected user
        if self.request.user.is_authenticated():
            return self.queryset.filter(user=self.request.user)
        # otherwise return nothing
        return UserService.objects.none()


class UserServiceCreateView(CreateView):
    form_class = UserServiceForm
    template_name = "services/add_service.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return HttpResponseRedirect('/service/add/thanks/')

    def get_context_data(self, **kw):
        context = super(UserServiceCreateView, self).get_context_data(**kw)
        context['action'] = 'add_service'
        return context


class UserServiceUpdateView(UpdateView):
    form_class = UserServiceForm
    template_name = "services/add_service.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kw):
        return super(UserServiceUpdateView, self).dispatch(*args, **kw)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return HttpResponseRedirect('/service/edit/thanks/')

    def get_object(self, queryset=None):
        obj = UserService.objects.get(pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kw):
        context = super(UserServiceUpdateView, self).get_context_data(**kw)
        context['action'] = 'edit_service'
        return context


class UserServiceDeleteView(DeleteView):
    queryset = UserService.objects.all()
    template_name = "services/delete_service.html"
    success_url = '/service/delete/thanks/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceDeleteView, self).dispatch(*args, **kwargs)


class UserServiceAddedTemplateView(TemplateView):
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(UserServiceAddedTemplateView, self).\
                                                    get_context_data(**kw)
        context['sentance'] = 'Your service has been successfully created'
        return context


class UserServiceEditedTemplateView(TemplateView):
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(UserServiceEditedTemplateView, self).\
                                                    get_context_data(**kw)
        context['sentance'] = 'Your service has been successfully modified'
        return context


class UserServiceDeletedTemplateView(TemplateView):
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(UserServiceDeletedTemplateView, self).\
                                                    get_context_data(**kw)
        context['sentance'] = 'Your service has been successfully deleted'
        return context


class UserServiceIndexView(ListView):
    """
        list of all available services activated from the admin
    """
    context_object_name = "services_list"
    queryset = ThServices.objects.all()
    template_name = "services/index.html"

    def get_queryset(self):
        # get the Service of the connected user
        # if self.request.user.is_authenticated():
        #    return self.queryset.filter(user=self.request.user)
        # otherwise return nothing
        return ThServices.objects.none()


from .forms import rss
from .forms import evernote
from .forms import ServicesForm

FORMS = [("rss", rss.RssForm),
         ("evernote", evernote.EvernoteForm),
         ("services", ServicesForm),
]
TEMPLATES = {
         '0': 'rss/wz-rss-form.html',
         '1': 'evernote/wz-evernote-form.html',
         '2': 'services_wizard/wz-description.html'
}


class UserServiceWizard(SessionWizardView):
    instance = None

    def get_form_instance(self, step):
        """
        Provides us with an instance of the Project Model to save on completion
        """
        if self.instance is None:
            self.instance = TriggerService()
        return self.instance

    def done(self, form_list, **kwargs):
        """
        Save info to the DB
        """
        print kwargs
        service = self.instance
        service.provider_id = ThServices.objects.get(name='rss').id
        service.consummer_id = ThServices.objects.get(name='evernote').id
        service.user = self.request.user
        service.save()
        return HttpResponseRedirect('/')

    def get_template_names(self):
        """
        Custom templates for the different steps
        """
        # print settings.TH_WIZARD_TPL
        # from django.conf import settings
        return [TEMPLATES[self.steps.current]]
