# coding: utf-8
from django.views.generic import TemplateView, ListView
from django.core.cache import caches
from django.conf import settings

from th_rss.models import Rss
from django_th.models import TriggerService

import django_th
cache = caches['th_rss']


class MyRssFeed(TemplateView):
    """
        page to display its RSS from any service
    """
    template_name = "rss/my_feed.html"

    def get_context_data(self, **kw):
        context = super(MyRssFeed, self).get_context_data(**kw)

        if 'uuid' in kw:
            # get the uuid from the Rss model
            rss = Rss.objects.get(uuid=kw['uuid'])
            # get its related Trigger where Provider use RSS
            trigger = TriggerService.objects.get(id=rss.trigger_id)
            # cut 'Service' to get the service name itself
            provider = trigger.provider.name.name.split('Service')[1].lower()
            pattern = 'th_{provider}_{id}'.format(provider=provider,
                                                  id=rss.trigger_id)
            context['data'] = cache.get(pattern)
            context['uuid'] = kw['uuid']
            context['last_build_date'] = trigger.date_triggered
        context['lang'] = settings.LANGUAGE_CODE
        context['version'] = django_th.__version__
        return context


class MyRssFeeds(ListView):
    """
        page to display all existing UUID from all RSS
    """
    context_object_name = "rss_list"
    queryset = TriggerService.objects.all()
    template_name = "rss/my_feeds.html"
    paginate_by = 3

    def get_paginate_by(self, queryset):
        """
            Get the number of items to paginate by,
            from the settings
        """
        return settings.DJANGO_TH.get('paginate_by', self.paginate_by)

    def get_queryset(self):
        # connected ?
        if self.request.user.is_authenticated():
            # get the Trigger that are MINE and where the CONSUMER is
            # the ServiceRss
            triggers = self.queryset.filter(user=self.request.user,
                                            consumer__name='ServiceRss')
            rss = []
            for trigger in triggers:
                rss.append(Rss.objects.get(trigger_id=trigger.id))
            return rss
        # otherwise return nothing when user is not connected
        return TriggerService.objects.none()
