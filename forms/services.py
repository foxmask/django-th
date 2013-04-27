# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from ..models import ServicesActivated


def available_services():
    """
        get the available services to be activated

        read the models dir to find the services installed
        to be added to the system by the administrator
    """
    all_datas = ()
    data = ()

    for class_path in settings.TH_SERVICES:
        module_name, class_name = class_path.rsplit('.', 1)
        prefix, service_name = class_name.rsplit('Service', 1)
        data = (class_name, service_name)
        all_datas = (data,) + all_datas
    return all_datas


class ServicesAdminForm(forms.ModelForm):
    """
        get the list of the available services (the activated one)
    """
    class Meta:
        model = ServicesActivated

    status_values = (('0', 'Disabled'), (1, 'Enabled'))
    status = forms.ChoiceField(status_values)
    name = forms.ChoiceField(available_services())
