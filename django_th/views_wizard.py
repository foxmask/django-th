from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django_th.models import TriggerService, UserService
from django_th.forms.wizard import ConsumerForm
from django_th.tools import get_service, class_for_name
from django_th.services import default_provider


"""
   Part III : Service Wizard
"""


class UserServiceWizard(SessionWizardView):

    def get_template_names(self):
        # name to find template :
        # form_name/wz-step-form.html
        # the form_name should be formed by the name of the service + form
        # for example :
        # rss/wz-1-form.html
        # rss/wz-3-form.html
        # evernote/wz-1-form.html
        # evernote/wz-3-form.html
        if self.steps.current in ('0', '2', '4'):
            folder = 'services_wizard'
        else:
            data = self.get_cleaned_data_for_step(self.get_prev_step(
                self.steps.current))
            if data.get('provider'):
                folder = str(data.get('provider')).split('Service')[1]
            elif data.get('consumer'):
                folder = str(data.get('consumer')).split('Service')[1]

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
            service_name = str(prev_data.get('provider')).split('Service')[1]
            class_name = 'th_' + service_name.lower() + '.forms'
            form_name = service_name + 'ProviderForm'
            form_class = class_for_name(class_name, form_name)
            form = form_class(data)

        elif step == '2':
            step0_data = self.get_cleaned_data_for_step('0')
            form = ConsumerForm(
                data, initial={'provider': step0_data.get('provider')})

        elif step == '3':

            prev_data = self.get_cleaned_data_for_step('2')
            service_name = str(prev_data.get('consumer')).split('Service')[1]
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
                    name=data.get('provider'),
                    user=self.request.user.id)
                model_provider = get_service(data.get('provider'), 'models')
            # get the service we selected at step 2 : consumer
            elif i == 2:
                trigger_consumer = UserService.objects.get(
                    name=data.get('consumer'),
                    user=self.request.user.id)
                model_consumer = get_service(data.get('consumer'), 'models')
            # get the description we gave for the trigger
            elif i == 4:
                trigger_description = data.get('description')
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
    default_provider.load_services()
    service_name = kwargs.get('service_name')
    service_object = default_provider.get_service(service_name)
    lets_callback = getattr(service_object, 'callback')
    # call the auth func from this class
    # and redirect to the external service page
    # to auth the application django-th to access to the user
    # account details
    return render_to_response(lets_callback(request))
