# coding: utf-8
from django.views.generic import TemplateView
from django.core.cache import caches
from django.conf import settings

import django_th
cache = caches['th_rss']


class MyRssFeeds(TemplateView):
    """
        page to display its RSS from any service
    """
    template_name = "rss/my_feeds.html"

    def get_context_data(self, **kw):
        context = super(MyRssFeeds, self).get_context_data(**kw)

        data = cache.get('th_rss_uuid_{}'.format(kw['uuid']))

        context = {'data': '', 'uuid': '', 'last_build_date': ''}
        if 'uuid' in kw:
            context['data'] = data
            context['uuid'] = kw['uuid']
        context['lang'] = settings.LANGUAGE_CODE
        context['version'] = django_th.__version__
        # @TODO get the last triggered date
        # context['last_build_date'] = data['date_triggered']

        return context
