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


class NameListFilter(admin.SimpleListFilter):
    title = 'name'
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        if request.GET.get('user__id__exact'):
            user_set = set([s.name.name for s in UserService.objects
                           .filter(user_id__exact=int(request.GET.get(
                                'user__id__exact')))])
        else:
            user_set = set([s.name.name for s in UserService.objects.all()])
        return [(i, i) for i in user_set]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name=self.value())
        return queryset


class UserServiceAdmin(admin.ModelAdmin):
    """
        get the list of the User Service
    """
    list_display = ('user', 'name', 'token')
    list_filter = ['user', NameListFilter]


class ProviderServiceListFilter(admin.SimpleListFilter):
    title = 'provider'
    parameter_name = 'provider'

    def lookups(self, request, model_admin):
        service_set = set([s for s in ServicesActivated.objects.all()])
        return [(i, i) for i in service_set]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(provider__name=self.value())
        else:
            return queryset


class ComsumerServiceListFilter(admin.SimpleListFilter):
    title = 'consumer'
    parameter_name = 'consumer'

    def lookups(self, request, model_admin):
        service_set = set([s for s in ServicesActivated.objects.all()])
        return [(i, i) for i in service_set]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(consumer__name=self.value())
        else:
            return queryset


class TriggerServiceAdmin(admin.ModelAdmin):
    """
        get the list of the User Service
    """
    list_display = ('user', 'provider', 'consumer', 'description',
                    'date_created', 'date_triggered', 'status')
    list_filter = [
        ('user', admin.RelatedOnlyFieldListFilter),
        ProviderServiceListFilter,
        ComsumerServiceListFilter,
        'status'
    ]


admin.site.register(ServicesActivated, ServicesManagedAdmin)
admin.site.register(UserService, UserServiceAdmin)
admin.site.register(TriggerService, TriggerServiceAdmin)
