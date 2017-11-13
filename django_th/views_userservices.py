# coding: utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import ListView

from django_th.models import UserService, ServicesActivated
from django_th.forms.base import UserServiceForm
from django_th.services import default_provider

"""
   Part II : User Service
"""


def renew_service(request, pk):
    """
        renew an existing service
        :param request object
        :param pk: the primary key of the service to renew
        :type pk: int
    """
    default_provider.load_services()
    service = get_object_or_404(ServicesActivated, pk=pk)
    service_name = str(service.name)
    service_object = default_provider.get_service(service_name)
    lets_auth = getattr(service_object, 'auth')
    getattr(service_object, 'reset_failed')(pk=pk)
    return redirect(lets_auth(request))


class UserServiceMixin(object):
    """
        Mixin for UpdateView and DeleteView
    """
    queryset = UserService.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceMixin, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # get the Service of the connected user
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user, id=self.kwargs.get('pk'))
        # otherwise return nothing
        return UserService.objects.none()


class UserServiceListView(ListView):
    """
        List of the services activated by the user
    """
    context_object_name = "services_list"
    queryset = UserService.objects.all()
    template_name = "services/services.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # get the Service of the connected user
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user).order_by('name')
        # otherwise return nothing
        return UserService.objects.none()

    def get_context_data(self, **kw):
        context = super(UserServiceListView, self).get_context_data(**kw)
        if self.request.user.is_authenticated:
            service_list_remaining = ServicesActivated.objects.exclude(
                name__in=self.queryset.values_list('name').filter(user=self.request.user).order_by('name'))
            context['service_list_remaining'] = service_list_remaining

        return context


class UserServiceCreateView(CreateView):
    """
        Form to add a service
    """
    form_class = UserServiceForm
    template_name = "services/service_form.html"

    def get_context_data(self, **kwargs):
        context = super(UserServiceCreateView, self).get_context_data(**kwargs)
        service_name = self.kwargs.get('service_name')
        get_object_or_404(ServicesActivated, name=service_name)
        context['service_name_alone'] = service_name.rsplit('Service')[1]
        context['service_name'] = service_name
        context['SERVICES_AUTH'] = settings.SERVICES_AUTH
        context['SERVICES_HOSTED_WITH_AUTH'] = settings.SERVICES_HOSTED_WITH_AUTH
        context['SERVICES_NEUTRAL'] = settings.SERVICES_NEUTRAL
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        name = self.kwargs.get('service_name')
        user = self.request.user
        if UserService.objects.filter(name=name, user=user).exists():
            messages.warning(self.request, _('Service %s already activated') % name.split('Service')[1])
            return HttpResponseRedirect(reverse('user_services'))
        return super(UserServiceCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data.get('name').name
        user = self.request.user
        form.save(user=user, service_name=self.kwargs.get('service_name'))

        sa = ServicesActivated.objects.get(name=name)
        # let's build the 'call' of the auth method
        # which own to a Service Class
        if sa.auth_required:
            # use the default_provider to get the object from the ServiceXXX
            default_provider.load_services()
            service_object = default_provider.get_service(str(name))
            # get the class object
            lets_auth = getattr(service_object, 'auth')
            # call the auth func from this class
            # and redirect to the external service page
            # to auth the application django-th to access to the user
            # account details
            return redirect(lets_auth(self.request))
        messages.success(self.request, _('Service %s activated successfully') % name.split('Service')[1])
        return HttpResponseRedirect(reverse('user_services'))

    def get_form_kwargs(self):
        kwargs = super(UserServiceCreateView, self).get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        kwargs['initial']['name'] = self.kwargs.get('service_name')
        return kwargs


class UserServiceUpdateView(UserServiceMixin, UpdateView):
    """
        Form to edit a service
    """
    form_class = UserServiceForm
    template_name = "services/service_form.html"

    def get_success_url(self):
        return reverse("user_services")

    def get_context_data(self, **kwargs):
        """
        push data from settings and from the current object, in the current
        context
        :param kwargs:
        :return:
        """
        context = super(UserServiceUpdateView, self).get_context_data(**kwargs)
        context['service_name_alone'] = self.object.name.name.rsplit('Service')[1]
        context['service_name'] = self.object.name.name
        context['SERVICES_AUTH'] = settings.SERVICES_AUTH
        context['SERVICES_HOSTED_WITH_AUTH'] = settings.SERVICES_HOSTED_WITH_AUTH
        context['SERVICES_NEUTRAL'] = settings.SERVICES_NEUTRAL

        context['action'] = 'edit'
        return context

    def get_form_kwargs(self):
        """
        initialize default value that won't be displayed
        :return:
        """
        kwargs = super(UserServiceUpdateView, self).get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        kwargs['initial']['name'] = self.object.name
        return kwargs

    def form_valid(self, form):
        """
        save the data
        :param form:
        :return:
        """
        # 'name' is injected in the clean() of the form line 56
        name = form.cleaned_data.get('name').name
        user = self.request.user
        form.save(user=user, service_name=name)
        messages.success(self.request, _('Service %s modified successfully') % name.split('Service')[1])
        return HttpResponseRedirect(reverse('user_services'))


class UserServiceDeleteView(UserServiceMixin, DeleteView):
    """
        page to delete a service
    """
    template_name = "services/delete_service.html"
    success_url = reverse_lazy("service_delete_thanks")

    def get_success_url(self):
        messages.success(self.request, _('Service %s deleted successfully') % self.object.name.name.split('Service')[1])
        return reverse("user_services")
