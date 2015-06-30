from django import forms

from th_holidays.models import Holidays


class HolidaysForm(forms.ModelForm):
    """
        Form to enable/disable the feature
    """
    class Meta:
        """
            model without any field
        """
        model = Holidays
        exclude = ['trigger', 'user', 'status']
