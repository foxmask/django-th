# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render_to_response, render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, ListView
from django.views.generic import TemplateView, UpdateView
from django.db.models import Q
from django.utils.translation import ugettext as _
from formtools.wizard.views import SessionWizardView

# trigger_happy
from django_th.models import TriggerService, UserService, ServicesActivated
from django_th.forms.base import UserServiceForm, TriggerServiceForm
from django_th.forms.wizard import ConsumerForm

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
    """
        Import a class dynamically
        :param module_name: the name of a module
        :param class_name: the name of a class
        :type module_name: string
        :type class_name: string
        :return: Return the value of the named attribute of object.
        :rtype: object
    """
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def get_service(service, model_form='models', form_name=''):
    """
        get the service name then load the model
        :param service: the service name
        :param model_form: could be 'models' or 'forms'
        :param form_name: the name of the form is model_form is 'forms'
        :type service: string
        :type model_form: string
        :type form_name: string
        :return: the object of the spotted Class.
        :rtype: object

        :Example:

        class_name could be :
            th_rss.models
            th_rss.forms
        service_name could be :
            ServiceRss
        then could call :
            Rss+ProviderForm
            Evernote+ConsumerForm
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
    return HttpResponseRedirect(reverse('base'))


def trigger_on_off(request, trigger_id):
    """
        enable/disable the status of the trigger then go back home
        :param trigger_id: the trigger ID to switch the status to True or False
        :type trigger_id: int
    """
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
    trigger.save()

    return render(request, 'triggers/trigger_line.html',
                           {'trigger': trigger,
                            'title': title,
                            'title_trigger': title_trigger,
                            'btn': btn})


def service_related_triggers_switch_to(request, user_service_id, switch):
    """
        switch the status of all the triggers related to the service, then go back home
        :param service_id: the service ID to switch the status to True or False of all the related trigger
        :type service_id: int
        :param switch: the switch value
        :type switch: string off or on
    """
    status = True
    if switch == 'off':
        status = False

    TriggerService.objects.filter(provider__id=user_service_id).update(status=status)
    TriggerService.objects.filter(consumer__id=user_service_id).update(status=status)

    return HttpResponseRedirect(reverse('user_services'))



def trigger_switch_all_to(request, switch):
    """
        switch the status of all the triggers then go back home
        :param switch: the switch value
        :type switch: string off or on
    """
    status = True
    if switch == 'off':
        status = False
    triggers = TriggerService.objects.all()
    for trigger in triggers:
        trigger.status = status
        trigger.save()

    return HttpResponseRedirect(reverse('base'))


def list_services(request, step):
    """
        get the activated services added from the administrator
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


def renew_service(request, pk):
    """
        renew an existing service
        :param pk: the primary key of the service to renew
        :type pk: int
    """
    service = get_object_or_404(ServicesActivated, pk=pk)
    service_name = str(service.name)
    service_object = default_provider.get_service(service_name)
    lets_auth = getattr(service_object, 'auth')
    return redirect(lets_auth(request))


#*************************************
#  Part I : the Triggers
#*************************************


def trigger_edit(request, trigger_id, edit_what):
    """
        edit the provider
        :param trigger_id: ID of the trigger to edit
        :param edit_what: edit a 'Provider' or 'Consumer' ?
        :type trigger_id: int
        :type edit_what: string
    """
    if edit_what not in ('Provider', 'Consumer'):
        #bad request
        return redirect('base')

    # get the trigger object
    service = TriggerService.objects.get(id=trigger_id)

    if edit_what == 'Consumer':
        # get the service name
        service_name = str(service.consumer.name.name).split('Service')[1]
        # get the model of this service
        model = get_service(service.consumer.name.name)
    else:
        # get the service name
        service_name = str(service.provider.name.name).split('Service')[1]
        # get the model of this service
        model = get_service(service.provider.name.name)

    # get the data of this service linked to that trigger
    data = model.objects.get(trigger_id=trigger_id)

    template_name = service_name.lower() + '/edit_' + edit_what.lower() + ".html"

    if request.method == 'POST':
        if edit_what == 'Consumer':
            form = get_service(
                service.consumer.name.name, 'forms', edit_what + 'Form')(
                request.POST, instance=data)
        else:
            form = get_service(
                service.provider.name.name, 'forms', edit_what + 'Form')(
                request.POST, instance=data)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('trigger_edit_thanks'))
    else:
        if edit_what == 'Consumer':
            form = get_service(
                service.consumer.name.name, 'forms', edit_what + 'Form')(
                instance=data)
        else:
            form = get_service(
                service.provider.name.name, 'forms', edit_what + 'Form')(
                instance=data)

    context = {'description': service.description, 'edit_what': edit_what}
    return render(request, template_name, {'form': form, 'context': context})


class TriggerListView(ListView):
    """
        list of Triggers
        the list can be filtered by service
    """
    context_object_name = "triggers_list"
    queryset = TriggerService.objects.all()
    template_name = "home.html"
    paginate_by = 3

    def get_queryset(self):
        trigger_filtered_by = None
        # by default, sort by date_created
        trigger_ordered_by = (str('-date_created'), )
        # get the Trigger of the connected user
        if self.request.user.is_authenticated():
            # if the user selected a filter, get its ID
            if 'trigger_filtered_by' in self.kwargs:
                user_service = UserService.objects.filter(
                    user=self.request.user,
                    name=self.kwargs['trigger_filtered_by'])
                trigger_filtered_by = user_service[0].id

            if 'trigger_ordered_by' in self.kwargs:
                """
                    sort by 'name' property in the related model UserService
                """
                order_by = str(self.kwargs['trigger_ordered_by'] + "__name")
                # append to the tuple, the selected 'trigger_ordered_by'
                # choosen in the dropdown
                trigger_ordered_by = (order_by, ) + trigger_ordered_by

            # no filter selected
            if trigger_filtered_by is None:
                return self.queryset.filter(user=self.request.user).order_by(*trigger_ordered_by).select_related('consumer__name', 'provider__name')

            # filter selected : display all related triggers
            else:
                # here the queryset will do :
                # 1) get trigger of the connected user AND
                # 2) get the triggers where the provider OR the consumer match
                # the selected service
                return self.queryset.filter(user=self.request.user).filter(
                    Q(provider=trigger_filtered_by) |
                    Q(consumer=trigger_filtered_by)).order_by(*trigger_ordered_by).select_related('consumer__name', 'provider__name')
        # otherwise return nothing when user is not connected
        return TriggerService.objects.none()

    def get_context_data(self, **kw):
        """
            get the data of the view

            data are :
            1) number of triggers enabled
            2) number of triggers disabled
            3) number of activated services
            4) list of activated services by the connected user
        """
        triggers_enabled = triggers_disabled = services_activated = ()

        context = super(TriggerListView, self).get_context_data(**kw)
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

        return context


class TriggerUpdateView(UpdateView):
    """
        Form to update description
    """
    model = TriggerService
    form_class = TriggerServiceForm
    template_name = "triggers/edit_description_trigger.html"
    success_url = reverse_lazy("trigger_edit_thanks")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerUpdateView, self).dispatch(*args, **kwargs)


class TriggerEditedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
    template_name = "triggers/thanks_trigger.html"

    def get_context_data(self, **kw):
        context = super(TriggerEditedTemplateView, self).get_context_data(**kw)
        context['sentence'] = 'Your trigger has been successfully modified'
        return context


class TriggerDeleteView(DeleteView):
    """
        page to delete a trigger
    """
    model = TriggerService
    template_name = "triggers/delete_trigger.html"
    success_url = reverse_lazy("trigger_delete_thanks")

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TriggerDeleteView, self).dispatch(*args, **kwargs)


class TriggerDeletedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
    template_name = "triggers/thanks_trigger.html"

    def get_context_data(self, **kw):
        context = super(TriggerDeletedTemplateView, self).\
            get_context_data(**kw)
        context['sentence'] = 'Your trigger has been successfully deleted'
        return context


#*************************************
#  Part II : the UserServices
#*************************************
class UserServiceListView(ListView):
    """
        List of the services activated by the user
    """
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

            # get the activated services
            """
                Number of services activated
            """
            context['nb_services'] = nb_user_service

        return context


class UserServiceCreateView(CreateView):
    """
        Form to add a service
    """
    form_class = UserServiceForm
    template_name = "services/add_service.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)

        sa = ServicesActivated.objects.get(name=form.cleaned_data['name'].name)
        # let's build the 'call' of the auth method
        #  which owns to a ServiceXXX class
        if sa.auth_required:
            # use the default_provider to get the object from the ServiceXXX
            service_object = default_provider.get_service(
                str(form.cleaned_data['name'].name))
            # get the class object
            lets_auth = getattr(service_object, 'auth')
            # call the auth func from this class
            # and redirect to the external service page
            # to auth the application django-th to access to the user
            # account details
            return redirect(lets_auth(self.request))

        return HttpResponseRedirect(reverse('service_add_thanks'))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(UserServiceCreateView, self).get_form_kwargs(**kwargs)
        kwargs['initial']['user'] = self.request.user
        return kwargs


class UserServiceRenewTemplateView(TemplateView):
    """
        page to renew a service
        usefull when revoking has been done or made changes
    """
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(
            UserServiceRenewTemplateView, self).get_context_data(**kw)
        context['sentence'] = 'Your service has been successfully renewed'
        return context


class UserServiceDeleteView(DeleteView):
    """
        page to delete a service
    """
    model = UserService
    template_name = "services/delete_service.html"
    success_url = reverse_lazy("service_delete_thanks")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceDeleteView, self).dispatch(*args, **kwargs)


class UserServiceAddedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(UserServiceAddedTemplateView, self).\
            get_context_data(**kw)
        context['sentence'] = 'Your service has been successfully created'
        return context


class UserServiceDeletedTemplateView(TemplateView):
    """
        just a simple form to say thanks :P
    """
    template_name = "services/thanks_service.html"

    def get_context_data(self, **kw):
        context = super(UserServiceDeletedTemplateView, self).get_context_data(
            **kw)
        context['sentence'] = 'Your service has been successfully deleted'
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
        # rss/wz-1-form.html
        # rss/wz-3-form.html
        # evernote/wz-1-form.html
        # evernote/wz-3-form.html
        if self.steps.current in('0', '2', '4'):
            folder = 'services_wizard'
        else:
            data = self.get_cleaned_data_for_step(self.get_prev_step(
                self.steps.current))
            if 'provider' in data:
                folder = str(data['provider']).split('Service')[1]
            elif 'consumer' in data:
                folder = str(data['consumer']).split('Service')[1]

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
            form = ConsumerForm(
                data, initial={'provider': step0_data['provider']})

        elif step == '3':

            prev_data = self.get_cleaned_data_for_step('2')
            service_name = str(prev_data['consumer']).split('Service')[1]
            class_name = 'th_' + service_name.lower() + '.forms'
            form_name = service_name + 'ConsumerForm'
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
            3) get the infos from the "Provider" and "Consumer" services
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
                    user=self.request.user.id)
                model_provider = get_service(data['provider'], 'models')
            # get the service we selected at step 2 : consumer
            elif i == 2:
                trigger_consumer = UserService.objects.get(
                    name=data['consumer'],
                    user=self.request.user.id)
                model_consumer = get_service(data['consumer'], 'models')
            # get the description we gave for the trigger
            elif i == 4:
                trigger_description = data['description']
            i += 1

        # save the trigger
        trigger = TriggerService(
            provider=trigger_provider, consumer=trigger_consumer,
            user=self.request.user, status=True,
            description=trigger_description)
        trigger.save()

        model_fields = {}
        # get the datas from the form for Service related
        # save the related models to provider and consumer
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
            # get the data for the consumer service
            elif i == 3:
                for field in data:
                    model_fields.update({field: data[field]})
                model_fields.update({'trigger_id': trigger.id, 'status': True})
                model_consumer.objects.create(**model_fields)
            i += 1

        return HttpResponseRedirect(reverse('base'))


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
