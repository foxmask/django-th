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
    
    provider = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        super(ProviderForm, self).__init__(*args, **kwargs)
        self.fields['provider'].choices = self.activated_services()                

    class Meta:
        model = TriggerService
        fields = ('provider', )


class ConsummerForm(ServiceChoiceForm):

    consummer = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ConsummerForm, self).__init__(*args, **kwargs)
        self.fields['consummer'].choices = self.activated_services()

    class Meta:
        model = TriggerService
        fields = ('consummer', )


class DummyForm(forms.Form):
    pass
