# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django_th.models import ServicesActivated


def available_services():
    """
        get the available services to be activated

        read the models dir to find the services installed
        to be added to the system by the administrator
    """
    all_datas = ()
    data = ()

    for class_path in settings.TH_SERVICES:
        class_name = class_path.rsplit('.', 1)[1]
        # 2nd array position contains the name of the service
        data = (class_name, class_name.rsplit('Service', 1)[1])
        all_datas = (data,) + all_datas
    return all_datas


class ServicesAdminForm(forms.ModelForm):

    """
        get the list of the available services (the activated one)
    """
    class Meta:
        model = ServicesActivated
        exclude = ()

    status_values = ((0, 'Disabled'), (1, 'Enabled'))
    status = forms.ChoiceField(status_values)
    name = forms.ChoiceField(available_services())

    # todo : set the value of status when editing the object
