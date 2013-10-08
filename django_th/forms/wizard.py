from django import forms
from django_th.models import TriggerService, ServicesActivated


class ServiceChoiceForm(forms.ModelForm):

    def activated_services(self):
        """
            get the activated services added from the administrator
        """
        all_datas = ()
        data = ()
        services = ServicesActivated.objects.filter(status=1)
        for class_name in services:
            data = (class_name, class_name.name.rsplit('Service', 1)[1])
            all_datas = (data,) + all_datas
        return all_datas


class ProviderForm(ServiceChoiceForm):
    provider = forms.ModelChoiceField(
                        queryset=ServicesActivated.objects.filter(status=1))

    class Meta:
        model = TriggerService
        fields = ('provider', )


class ConsummerForm(ServiceChoiceForm):
    consummer = forms.ModelChoiceField(
                        queryset=ServicesActivated.objects.filter(status=1))

    class Meta:
        model = TriggerService
        fields = ('consummer', )


class DummyForm(forms.Form):
    pass
