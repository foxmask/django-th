# -*- coding: utf-8 -*-
from django import forms
from ..models.services import ServicesMgr


def available_services():
    """
        get the activated services

        read the models dir to find the services installed
        to be added to the system by the administrator
    """
    import os
    models_services_dir = os.path.dirname(os.path.abspath(__file__))
    models_services_dir = os.path.realpath(models_services_dir + '/../models')
    print models_services_dir
    all_datas = ()
    data = ()
    for model_file in os.listdir(models_services_dir):
        if not model_file in ('services.py', 'services.pyc',
                              '__init__.py', '__init__.pyc'):
            name, name_ext = model_file.rsplit('.', 1)
            if not name_ext == 'pyc':
                data = (name, name.capitalize())
                all_datas = (data,) + all_datas
    return all_datas


class ServicesAdminForm(forms.ModelForm):
    """
        get the list of the available services (the activated one)
    """
    class Meta:
        model = ServicesMgr
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    status_values = (('0', 'Disabled'), (1, 'Enabled'))
    status = forms.ChoiceField(status_values)
    name = forms.ChoiceField(available_services())
