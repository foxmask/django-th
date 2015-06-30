from django.conf.urls import patterns, url

from th_holidays.views import holidays, holidays_done

urlpatterns = \
    patterns('',
             url(r"^$", holidays, name="holidays",),
             url(r"^done/$", holidays_done, name="holidays_done",),
             )
