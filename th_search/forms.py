# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm


class TriggerHappySearchForm(SearchForm):

    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(
                            attrs={'type': 'search',
                                   'placeholder': _('Search for ...'),
                                   'class': 'form-control'}))

    def no_query_found(self):
        return self.searchqueryset.all()
