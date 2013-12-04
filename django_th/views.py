# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from django.contrib.formtools.wizard.views import SessionWizardView

# trigger_happy
from django_th.models import TriggerService, UserService, ServicesActivated
from django_th.forms.base import UserServiceForm
from django_th.forms.wizard import ConsummerForm

from django_th.services import default_provider


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.contrib.auth import logout

default_provider.load_services()


#*****************************
# Simple utility functions
#*****************************
import importlib


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def get_service(service, model_form='models', form_name=''):
    """
        get the service name then load the model
        class_name could be :
            th_rss.models
            th_rss.forms
        service_name could be :
            ServiceRss
        then could call :
            Rss+ProviderForm
            Evernote+ConsummerForm
    """
    service_name = str(service).split('Service')[1]

    class_name = 'th_' + service_name.lower() + '.' + model_form

    if model_form == 'forms':
        return class_for_name(class_name, service_name + form_name)
    else:
        return class_for_name(class_name, service_name)

#************************
# FBV : simple actions  *
#************************


def logout_view(request):
    """
        logout the user then redirect him to the home page
    """
    logout(request)
    return redirect('base')


def trigger_on_off(request, trigger_id):
    """
        switch the status of the trigger then go back home
    """
    trigger = TriggerService.objects.get(id=trigger_id)
    if trigger.status:
        trigger.status = False
    else:
        trigger.status = True
    trigger.save()

    return redirect('base')


def trigger_switch_all_to(request, switch):
    """
        switch the status of all the triggers then go back home
    """
    status = True
    if switch == 'off':
        status = False
    triggers = TriggerService.objects.all()
    for trigger in triggers:
        trigger.status = status
        trigger.save()

    return redirect('base')


def qty_services_activated(user):
    """
        get the quantity of activated services
    """
    return UserService.objects.filter(user=user)


def list_services(request, step):
    """
        get the activated services added from the administrator
    """
    # print request.request
    all_datas = []
    # data = ()

    if step == '0':
        services = ServicesActivated.objects.filter(status=1)
    elif step == '3':
        services = ServicesActivated.objects.filter(status=1,
                                                    id__iexact=request.id)
    for class_name in services:
        # data = (class_name, class_name.name.rsplit('Service', 1)[1])
        all_datas.append({class_name: class_name.name.rsplit('Service', 1)[1]})

    return all_datas


#*************************************
#  Part I : the Triggers
#*************************************


def trigger_edit_provider(request, trigger_id):
    service = TriggerService.objects.get(id=trigger_id)
    service_name = str(service.provider).split('Service')[1]
    model = get_service(service.provider)
    data = model.objects.get(trigger_id=trigger_id)

    if request.method == 'POST':
        form = get_service(service.provider, 'forms', 'ProviderForm')(
            request.POST, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/trigger/edit/thanks/')
    else:
        form = get_service(
            service.provider, 'forms', 'ProviderForm')(instance=data)
    context = {'description': service.description}
    return render(request, service_name.lower() + 'provider/edit_provider.html', {
        'form': form,
        'context': context
    })


def trigger_edit_consummer(request, trigger_id):
    service = TriggerService.objects.get(id=trigger_id)
    service_name = str(service.consummer).split('Service')[1]
    model = get_service(service.consummer)
    data = model.objects.get(trigger_id=trigger_id)

    if request.method == 'POST':
        form = get_service(service.consummer, 'forms', 'ConsummerForm')(
            request.POST, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/trigger/edit/thanks/')
    else:
        form = get_service(
            service.consummer, 'forms', 'ConsummerForm')(instance=data)
    context = {'description': service.description}
    return render(request, service_name.lower() + 'consummer/edit_consummer.html', {
        'form': form,
        'context': context
    })


class TriggerListView(ListView):
    context_object_name = "triggers_list"
    queryset = TriggerService.objects.all()
    template_name = "home.html"
    paginate_by = 7

    def get_queryset(self):
        # get the Trigger of the connected user
        if self.request.user.is_authenticated():
            return self.queryset.filter(user=self.request.user).\
                order_by('-date_created')
        # otherwise return nothing
        return TriggerService.objects.none()

    def get_context_data(self, **kw):
        triggers_enabled = triggers_disabled = services_activated = ()
        if self.request.user.is_authenticated():
            # get the enabled triggers
            triggers_enabled = TriggerService.objects.filter(
                user=self.request.user, status=1)
            # get the disabled triggers
            triggers_disabled = TriggerService.objects.filter(
                user=self.request.user, status=0)
            # get the activated services
            services_activated = qty_services_activated(self.request.user)
        context = super(TriggerListView, self).get_context_data(**kw)
        context['nb_triggers'] = {'enabled': len(triggers_enabled),
                                  'disabled': len(triggers_disabled)}
        context['nb_services'] = len(services_activated)
        return context


class TriggerUpdateView(UpdateView):
    queryset = TriggerService.objects.all()
    fields = ['description']
    template_name = "triggers/edit_description_trigger.html"
    success_url = '/trigger/edit/thanks/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerUpdateView, self).dispatch(*args, **kwargs)


class TriggerEditedTemplateView(TemplateView):
    template_name = "triggers/thanks_trigger.html"

    def get_context_data(self, **kw):
        context = super(TriggerEditedTemplateView, self).get_context_data(**kw)
        context['sentance'] = 'Your trigger has been successfully modified'
        return context


class TriggerDeleteView(DeleteView):
    queryset = TriggerService.objects.all()
    template_name = "triggers/delete_trigger.html"
    success_url = '/trigger/delete/thanks/'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerDeleteView, self).dispatch(*args, **kwargs)


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

    def get_context_data(self, **kw):
        context = super(UserServiceListView, self).get_context_data(**kw)
        if self.request.user.is_authenticated():
            activated_qs = ServicesActivated.objects.all()
            service_list_available = UserService.objects.filter(
                id__exact=None, name__in=activated_qs)
            nb_user_service = UserService.objects.filter(
                user=self.request.user).count()
            nb_service = ServicesActivated.objects.all().count()
            if nb_user_service == nb_service:
                context['action'] = 'hide'
            else:
                context['action'] = 'display'
            context['service_list_available'] = service_list_available
        return context


class UserServiceCreateView(CreateView):
    form_class = UserServiceForm
    template_name = "services/add_service.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)

        sa = ServicesActivated.objects.get(name=form.cleaned_data['name'])
        # let's build the 'call' of the auth method
        #  which owns to a ServiceXXX class
        if sa.auth_required:
            # use the default_provider to get the object from the ServiceXXX
            service_object = default_provider.get_service(
                str(form.cleaned_data['name']))
            # get the class object
            lets_auth = getattr(service_object, 'auth')
            # call the auth func from this class
            # and redirect to the external service page
            # to auth the application django-th to access to the user
            # account details
            return redirect(lets_auth(self.request))

        return HttpResponseRedirect('/service/add/thanks/')

    def get_context_data(self, **kw):
        context = super(UserServiceCreateView, self).get_context_data(**kw)
        context['action'] = 'add_service'
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(UserServiceCreateView, self).get_form_kwargs(**kwargs)
        kwargs['initial']['user'] = self.request.user
        return kwargs


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


class UserServiceDeletedTemplateView(TemplateView):
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(UserServiceDeletedTemplateView, self).get_context_data(
            **kw)
        context['sentance'] = 'Your service has been successfully deleted'
        return context

#*************************************
#  Part III : Service Wizard
#*************************************


class UserServiceWizard(SessionWizardView):

    def get_template_names(self):
        # name to find template :
        #  form_name/wz-step-form.html
        #  the form_name should be formed by the name of the service + form
        #  for example :
        # rssform/wz-1-form.html
        # rssform/wz-3-form.html
        # evernoteform/wz-1-form.html
        # evernoteform/wz-3-form.html
        if self.steps.current in('0', '2', '4'):
            folder = 'services_wizard'
        else:
            data = self.get_cleaned_data_for_step(self.get_prev_step(
                self.steps.current))
            if 'provider' in data:
                folder = str(data['provider']).split('Service')[1] + 'form'
            elif 'consummer' in data:
                folder = str(data['consummer']).split('Service')[1] + 'form'

        return '%s/wz-%s-form.html' % (folder.lower(), self.steps.current)

    def get_form(self, step=None, data=None, files=None):
        """
            change the form instance dynamically from the data we entered
            at the previous step
        """
        if step is None:
            step = self.steps.current

        if step == '1':

            prev_data = self.get_cleaned_data_for_step('0')
            service_name = str(prev_data['provider']).split('Service')[1]
            class_name = 'th_' + service_name.lower() + '.forms'
            form_name = service_name + 'ProviderForm'
            form_class = class_for_name(class_name, form_name)
            form = form_class(data)

        elif step == '2':
            step0_data = self.get_cleaned_data_for_step('0')
            form = ConsummerForm(
                data, initial={'provider': step0_data['provider']})

        elif step == '3':

            prev_data = self.get_cleaned_data_for_step('2')
            service_name = str(prev_data['consummer']).split('Service')[1]
            class_name = 'th_' + service_name.lower() + '.forms'
            form_name = service_name + 'ConsummerForm'
            form_class = class_for_name(class_name, form_name)
            form = form_class(data)

        else:
            form = super(UserServiceWizard, self).get_form(step, data, files)

        return form

    def done(self, form_list, **kwargs):
        """
            Save info to the DB
            The process is :
            1) get the infos for the Trigger from step 0, 2, 4
            2) save it to TriggerService
            3) get the infos from the "Provider" and "Consummer" services
            at step 1 and 3
            4) save all of them
        """
        # get the datas from the form for TriggerService
        i = 0
        for form in form_list:
            # cleaning
            data = form.cleaned_data
            # get the service we selected at step 0 : provider
            if i == 0:
                trigger_provider = UserService.objects.get(
                    name=data['provider'],
                    user=self.request.user)
                model_provider = get_service(data['provider'], 'models')
            # get the service we selected at step 2 : consummer
            elif i == 2:
                trigger_consummer = UserService.objects.get(
                    name=data['consummer'],
                    user=self.request.user)
                model_consummer = get_service(data['consummer'], 'models')
            # get the description we gave for the trigger
            elif i == 4:
                trigger_description = data['description']
            i += 1

        # save the trigger
        trigger = TriggerService(
            provider=trigger_provider, consummer=trigger_consummer,
            user=self.request.user, status=True,
            description=trigger_description)
        trigger.save()

        model_fields = {}
        # get the datas from the form for Service related
        # save the related models to provider and consummer
        i = 0
        for form in form_list:
            model_fields = {}
            data = form.cleaned_data
            # get the data for the provider service
            if i == 1:
                for field in data:
                    model_fields.update({field: data[field]})
                model_fields.update({'trigger_id': trigger.id, 'status': True})
                model_provider.objects.create(**model_fields)
            # get the data for the consummer service
            elif i == 3:
                for field in data:
                    model_fields.update({field: data[field]})
                model_fields.update({'trigger_id': trigger.id, 'status': True})
                model_consummer.objects.create(**model_fields)
            i += 1

        return HttpResponseRedirect('/')


def finalcallback(request, **kwargs):
    """
        let's do the callback of the related service after
        the auth request from UserServiceCreateView
    """
    service_name = kwargs['service_name']
    service_object = default_provider.get_service(service_name)
    lets_callback = getattr(service_object, 'callback')
    # call the auth func from this class
    # and redirect to the external service page
    # to auth the application django-th to access to the user
    # account details
    return render_to_response(lets_callback(request))
