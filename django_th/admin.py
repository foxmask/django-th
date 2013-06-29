from django.contrib import admin

from django_th.forms.services import ServicesAdminForm
from django_th.models import ServicesActivated


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

admin.site.register(ServicesActivated, ServicesManagedAdmin)
