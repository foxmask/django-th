from django.contrib import admin

from django_th.forms.services import ServicesAdminForm
from django_th.models import ServicesActivated
from django_th.models import UserService


class ServicesManagedAdmin(admin.ModelAdmin):
    """
        get the list of the available services (the activated one)
    """
    list_display = ('name', 'description', 'status', 'auth_required')

    add_form = ServicesAdminForm
    view_form = ServicesAdminForm

    def get_form(self, request, obj=None, **args):
        defaults = {}
        if obj is None:
            defaults.update({'form': self.add_form, })
        else:
            defaults.update({'form': self.view_form, })
        defaults.update(args)
        return super(ServicesManagedAdmin, self).get_form(request, obj,
                                                          **defaults)


class UserServiceAdmin(admin.ModelAdmin):
    """
        get the list of the User Service
    """
    list_display = ('user', 'name', 'token')
    list_filter = ['user', 'name']


admin.site.register(ServicesActivated, ServicesManagedAdmin)
admin.site.register(UserService, UserServiceAdmin)
