from django.contrib import admin

from django_th.forms.services import ServicesAdminForm
from django_th.models import ServicesActivated
from django_th.models import UserService
from django_th.models import TriggerService


class ServicesManagedAdmin(admin.ModelAdmin):

    """
        get the list of the available services (the activated one)
    """

    def make_status_enable(self, request, queryset):
        rows_updated = queryset.update(status=True)
        if rows_updated == 1:
            message_bit = "1 service was"
        else:
            message_bit = "%s services were" % rows_updated
        self.message_user(
            request, "%s successfully marked as enabled." % message_bit)

    def make_status_disable(self, request, queryset):
        rows_updated = queryset.update(status=False)

        if rows_updated == 1:
            message_bit = "1 service was"
        else:
            message_bit = "%s services were" % rows_updated
        self.message_user(
            request, "%s successfully marked as disabled." % message_bit)

    make_status_enable.short_description = "Status Enable"
    make_status_disable.short_description = "Status Disable"
    list_display = ('name', 'description', 'status',
                    'auth_required', 'self_hosted')

    actions = [make_status_enable, make_status_disable]
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


class TriggerServiceAdmin(admin.ModelAdmin):

    """
        get the list of the User Service
    """
    list_display = ('user', 'provider', 'consumer', 'description',
                    'date_created', 'date_triggered', 'status')
    list_filter = ['user', 'provider', 'consumer', 'status']


admin.site.register(ServicesActivated, ServicesManagedAdmin)
admin.site.register(UserService, UserServiceAdmin)
admin.site.register(TriggerService, TriggerServiceAdmin)
