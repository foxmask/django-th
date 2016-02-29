from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView
from django.views.generic import ListView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse

from django.http import HttpResponseRedirect

from django_th.models import UserService, ServicesActivated
from django_th.forms.base import UserServiceForm
from django_th.services import default_provider


"""
   Part II : User Service
"""


def renew_service(request, pk):
    """
        renew an existing service
        :param pk: the primary key of the service to renew
        :type pk: int
    """
    default_provider.load_services()
    service = get_object_or_404(ServicesActivated, pk=pk)
    service_name = str(service.name)
    service_object = default_provider.get_service(service_name)
    lets_auth = getattr(service_object, 'auth')
    return redirect(lets_auth(request))


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
        default_provider.load_services()
        self.object = form.save(user=self.request.user)

        sa = ServicesActivated.objects.get(name=form.cleaned_data['name'].name)
        # let's build the 'call' of the auth method
        # which own to a Service Class
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

    def get_form_kwargs(self):
        kwargs = super(UserServiceCreateView, self).get_form_kwargs()
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
