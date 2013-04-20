from django.contrib import admin
from .models.services import ThServices

from .models.rss import ServiceRss
from .models.evernote import ServiceEvernote
from forms import ServicesManagedForm


class ServicesManagedAdmin(admin.ModelAdmin):
    """
        get the list of the available services (the activated one)
    """
    list_display = ('name', 'my_status')

    add_form = ServicesManagedForm
    view_form = ServicesManagedForm

    def get_form(self, request, obj=None, **args):
        defaults = {}
        if obj is None:
            defaults.update({'form': self.add_form, })
        else:
            defaults.update({'form': self.view_form, })
        defaults.update(args)
        return super(ServicesManagedAdmin, self).get_form(request, obj, \
                                                          **defaults)

admin.site.register(ThServices, ServicesManagedAdmin)
