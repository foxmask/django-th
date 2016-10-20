from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import ListView

from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect

from django_th.models import UserService, ServicesActivated
from django_th.forms.base import UserServiceForm, activated_services
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

            if self.kwargs:
                context['sentence'] = _('Your service has been successfully ')
                if self.kwargs.get('action') in ('renewed', 'deleted',
                                                 'edited', 'added'):
                    context['sentence'] += self.kwargs.get('action')

        return context


class UserServiceCreateView(CreateView):
    """
        Form to add a service
    """
    form_class = UserServiceForm
    template_name = "services/add_service.html"

    def get_context_data(self, **kwargs):
        context = super(UserServiceCreateView, self).get_context_data(**kwargs)
        context['services'] = len(activated_services(self.request.user))
        print(context)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserServiceCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data.get('name').name
        user = self.request.user
        if UserService.objects.filter(name=name, user=user).exists():
            from django.contrib import messages
            messages.warning(self.request, 'Service %s already activated' %
                             name.split('Service')[1])
            return HttpResponseRedirect(reverse('user_services'))
        else:
            form.save(user=user)

            sa = ServicesActivated.objects.get(
                name=form.cleaned_data.get('name').name)
            # let's build the 'call' of the auth method
            # which own to a Service Class
            if sa.auth_required:
                # use the default_provider to get the object from the ServiceXXX
                default_provider.load_services()
                service_object = default_provider.get_service(
                    str(form.cleaned_data.get('name').name))
                # get the class object
                lets_auth = getattr(service_object, 'auth')
                # call the auth func from this class
                # and redirect to the external service page
                # to auth the application django-th to access to the user
                # account details
                return redirect(lets_auth(self.request))

            return HttpResponseRedirect(reverse('user_services',
                                                args=['added']))

    def get_form_kwargs(self):
        kwargs = super(UserServiceCreateView, self).get_form_kwargs()
        kwargs['initial']['user'] = self.request.user
        return kwargs


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
        if self.request.user.is_authenticated():
            return self.queryset.filter(user=self.request.user,
                                        id=self.kwargs.get('pk'))
        # otherwise return nothing
        return UserService.objects.none()


class UserServiceUpdateView(UserServiceMixin, UpdateView):
    """
        Form to edit a service
    """
    fields = ['username', 'password',
              'client_secret', 'client_id', 'host',
              'token']
    template_name = "services/edit_service.html"

    def get_success_url(self):
        return reverse("user_services", args=["edited"])


class UserServiceDeleteView(UserServiceMixin, DeleteView):
    """
        page to delete a service
    """
    template_name = "services/delete_service.html"
    success_url = reverse_lazy("service_delete_thanks")

    def get_success_url(self):
        return reverse("user_services", args=["deleted"])
