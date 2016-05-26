# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


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
        return "Service Activated %s %s %s %s" % (self.name, self.status,
                                                  self.auth_required,
                                                  self.description)

    def __str__(self):
        return self.name


class UserService(models.Model):

    """
        UserService a model to link service and user
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    name = models.ForeignKey(
        ServicesActivated, to_field='name', related_name='+')
    username = models.CharField(
        _('username'), max_length=255, default='', blank=True)
    password = models.CharField(
        _('password'), max_length=128, default='', blank=True)
    host = models.CharField(_('host'), max_length=255, default='', blank=True)
    client_id = models.CharField(
        _('client id'), max_length=255, default='', blank=True)
    client_secret = models.CharField(
        _('client secret'), max_length=255, default='', blank=True)

    def show(self):
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

    def __str__(self):
        return "{} - {} - {} - {}".format(self.user,
                                          self.provider.name,
                                          self.consumer.name,
                                          self.description)

    def show(self):
        return "My Service {} {} {} {}".format(self.user,
                                               self.provider.name,
                                               self.consumer.name,
                                               self.description)
