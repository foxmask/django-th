# -*- coding: utf-8 -*-
from haystack import indexes

from django.utils import timezone

from django_th.models import TriggerService


class TriggerHappyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    provider = indexes.CharField(model_attr='provider__name')
    consumer = indexes.CharField(model_attr='consumer__name')
    description = indexes.CharField(model_attr='description')
    user = indexes.CharField(model_attr='user__id')
    date_created = indexes.DateField(model_attr='date_created')
    date_triggered = indexes.DateTimeField(model_attr='date_triggered')
    status = indexes.BooleanField(model_attr='status')

    def get_model(self):
        return TriggerService

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        now = timezone.now()
        return self.get_model().objects.filter(date_created__lte=now)
