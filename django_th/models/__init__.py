# coding: utf-8
import arrow

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from django_th.signals import digest_event
from django_th.tools import warn_user_and_admin

from logging import getLogger

logger = getLogger('django_th.trigger_happy')


class ServicesActivated(models.Model):

    """
        Services Activated from the admin
    """
    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField(default=False)
    auth_required = models.BooleanField(default=True)
    self_hosted = models.BooleanField(default=False)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    def show(self):
        """

        :return: string representing object
        """
        return "Service Activated %s %s %s %s" % (self.name, self.status,
                                                  self.auth_required,
                                                  self.description)

    def __str__(self):
        return self.name


class UserService(models.Model):

    """
        UserService a model to link service and user
    """
    DAY = 'd'
    WEEK = 'w'
    MONTH = 'm'
    NONE = 'n'
    DURATION = (
        (DAY, _('Day')),
        (WEEK, _('Week')),
        (MONTH, _('Month')),
        (NONE, _('None'))
    )

    user = models.ForeignKey(User)
    token = models.CharField(max_length=255, blank=True)
    name = models.ForeignKey(ServicesActivated, to_field='name', related_name='+')
    username = models.CharField(_('username'), max_length=255, default='', blank=True)
    password = models.CharField(_('password'), max_length=128, default='', blank=True)
    host = models.URLField(_('host'), default='', blank=True)
    client_id = models.CharField(_('client id'), max_length=255, default='', blank=True)
    client_secret = models.CharField(_('client secret'), max_length=255, default='', blank=True)
    duration = models.CharField(max_length=1, choices=DURATION, default=NONE)
    counter_ok = models.IntegerField(default=0)
    counter_ko = models.IntegerField(default=0)

    def show(self):
        """

        :return: string representing object
        """
        return "User Service %s %s %s" % (self.user, self.token, self.name)

    def __str__(self):
        return self.name.name


class TriggerService(models.Model):

    """
        TriggerService
    """
    provider = models.ForeignKey(UserService, related_name='+', blank=True)
    consumer = models.ForeignKey(UserService, related_name='+', blank=True)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    date_triggered = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    result = models.CharField(max_length=255, default='')
    date_result = models.DateTimeField(auto_now=True, null=True)
    provider_failed = models.IntegerField(db_index=True, default=0)
    consumer_failed = models.IntegerField(db_index=True, default=0)

    counter_ok = models.IntegerField(default=0)
    counter_ko = models.IntegerField(default=0)

    def show(self):
        """

        :return: string representing object
        """
        return "My Service %s - %s - %s - %s" % (self.user,
                                                 self.provider.name,
                                                 self.consumer.name,
                                                 self.description)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.user,
                                      self.provider.name,
                                      self.consumer.name,
                                      self.description)


class Digest(models.Model):
    """
    Digest service to store the data from other service
    """
    user = models.ForeignKey(User)
    title = models.CharField(max_length=600)
    link = models.URLField()
    duration = models.CharField(max_length=1)
    date_end = models.DateField()
    provider = models.CharField(max_length=40)

    def show(self):
        """

        :return: string representing object
        """
        return "Digest %s - %s - %s - %s - %s - %s" % (
            self.user, self.provider, self.title, self.link, self.duration,
            self.date_end)

    def __str__(self):
        return "%s - %s - %s - %s - %s - %s" % (
            self.user, self.provider, self.title, self.link, self.duration,
            self.date_end)


def update_result(trigger_id, msg, status):
    """
    :param trigger_id: trigger id
    :param msg: result msg
    :param status: status of the handling of the current trigger
    :return:
    """
    service = TriggerService.objects.get(id=trigger_id)
    # if status is True, reset *_failed counter
    if status:
        provider_failed = 0
        consumer_failed = 0
        counter_ok = service.counter_ok + 1
        counter_ko = service.counter_ko
    # otherwise, add 1 to the consumer_failed
    else:
        provider_failed = service.provider_failed
        consumer_failed = service.consumer_failed + 1
        counter_ok = service.counter_ko
        counter_ko = service.counter_ko + 1

        status = False if consumer_failed > settings.DJANGO_TH.get('failed_tries', 5) else True

        warn_user_and_admin('consumer', service)

    TriggerService.objects.filter(id=trigger_id).update(
        result=msg,
        date_result=now(),
        provider_failed=provider_failed,
        consumer_failed=consumer_failed,
        counter_ok=counter_ok,
        counter_ko=counter_ko,
        status=status)

    UserService.objects.filter(user=service.user, name=service.consumer.name).update(
        counter_ok=counter_ok,
        counter_ko=counter_ko)


def th_create_user_profile(sender, instance, created, **kwargs):
    # create the default service that does not
    # need any third party auth
    user = instance
    if user.last_login is None:
        for service in settings.SERVICES_NEUTRAL:
            try:
                sa = ServicesActivated.objects.get(name=service)
                UserService.objects.get_or_create(user=user, name=sa)
            except ObjectDoesNotExist:
                logger.debug("A new user %s has been connected but %s "
                             "could not be added to his services because "
                             "the service is present in th_settings.py file but not"
                             " activated from the Admin Panel" % (user, service))


post_save.connect(th_create_user_profile, sender=User, dispatch_uid="create_user_profile")


@receiver(digest_event)
def digest_save(sender, **kwargs):
    """

    :param sender:
    :param kwargs:
    :return:
    """
    # set the deadline of the publication of the digest data
    duration = kwargs.get('duration')
    if duration not in ('d', 'w', 'm'):
        return
    # get the current date
    now = arrow.utcnow().to(settings.TIME_ZONE)

    # set the deadline
    if duration == 'd':
        # set tomorrow
        tomorrow = now.shift(days=+1)
        date_end = tomorrow.date()  # noqa extrat the date part
    elif duration == 'w':
        # set next week
        next_week = now.shift(weeks=+1)
        date_end = next_week.date()
    else:
        # set next month
        next_month = now.shift(months=+1)
        date_end = next_month.date()

    Digest.objects.create(user=kwargs.get('user'),
                          title=kwargs.get('title'),
                          link=kwargs.get('link'),
                          duration=duration,
                          date_end=str(date_end),
                          provider=sender)
