from django import forms
from django_th.models import ServicesActivated
from django.utils.translation import ugettext_lazy as _


class ServiceChoiceForm(forms.Form):

    def activated_services(self, provider=None):
        """
            get the activated services added from the administrator
            :param provider: the selected provider
            :type provider: string
            :return: list of activated services
            :rtype: list
        """
        services = ServicesActivated.objects.filter(status=1)

        choices = []
        datas = ()

        if provider is not None:
            services = services.exclude(name__exact=provider)

        for class_name in services:
            datas = (class_name.name, class_name.name.rsplit('Service', 1)[1])
            choices.append(datas)

        return choices


class ProviderForm(ServiceChoiceForm):

    """
        Set some HTML class to the Provider form
    """
    provider = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ProviderForm, self).__init__(*args, **kwargs)
        self.fields['provider'].choices = self.activated_services()
        self.fields['provider'].widget.attrs['class'] = 'form-control'


class ConsumerForm(ServiceChoiceForm):

    """
        Set some HTML class to the Consumer form
    """
    consumer = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ConsumerForm, self).__init__(*args, **kwargs)
        # get the list of service without the one selected in
        # the provider form
        self.fields['consumer'].choices = self.activated_services(
            self.initial['provider'])
        self.fields['consumer'].widget.attrs['class'] = 'form-control'


class ServicesDescriptionForm(forms.Form):

    """
        Set some HTML class to the Service form
    """
    description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':
                                      _('A description for your new service')})
    )


class DummyForm(forms.Form):
    pass
