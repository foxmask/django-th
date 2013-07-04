# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class ServicesActivated(models.Model):
    """
    Services Activated from the admin
    # Create a ServicesActivated
    >>> from django_th.models import ServicesActivated
    >>> name = 'ServiceRss'
    >>> status = True
    >>> auth_required = True
    >>> description = 'RSS Feeds Service'
    >>> service_activated = ServicesActivated.objects.create(name=name, status=status, auth_required=auth_required, description=description)
    >>> service_activated.show()
    'Service Activated ServiceRss True True RSS Feeds Service'
    """
    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField()
    auth_required = models.BooleanField()
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    def show(self):
        return "Service Activated %s %s %s %s" % (self.name, self.status,
                                                  self.auth_required, self.description)

    def __unicode__(self):
        return "%s" % (self.name)


class UserProfile(models.Model):
    """
    Related user to handle his profile
    >>> from django_th.models import UserProfile
    >>> my_user = UserProfile.objects.create(user_id=999)
    >>> my_user.show()
    'User profile 999'
    """
    user = models.OneToOneField(User)

    def show(self):
        return "User profile %s" % (self.user_id)

    def __unicode__(self):
        return "%s" % (self.user)


class UserService(models.Model):
    """
    UserService a model to link service and user
    # Create a UserService
    >>> from django.contrib.auth.models import User
    >>> from django_th.models import UserProfile, UserService, ServicesActivated
    >>> my_user = User.objects.create(id=888,username='foxmask')
    >>> user1 = User.objects.get(id=888)
    >>> token = ''
    >>> name = 'ServiceRss1'
    >>> status = True
    >>> auth_required = False
    >>> description = 'RSS Feeds Service'
    >>> service_activated = ServicesActivated.objects.create(name=name, status=status, auth_required=auth_required, description=description)
    >>> name = ServicesActivated.objects.get(name='ServiceRss1')
    >>> user_service = UserService.objects.create(user=user1, token=token, name=name)
    >>> user_service.show()
    'User Service foxmask ServiceRss1'
    >>> token = 'foobar123'
    >>> name = 'ServiceEvernote1'
    >>> status = True
    >>> auth_required = True
    >>> description = 'Evernote Service'
    >>> service_activated = ServicesActivated.objects.create(name=name, status=status, auth_required=auth_required, description=description)
    >>> name = ServicesActivated.objects.get(name='ServiceEvernote1')
    >>> user_service = UserService.objects.create(user=user1, token=token, name=name)
    >>> user_service.show()
    'User Service foxmask foobar123 ServiceEvernote1'
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    name = models.ForeignKey(
        ServicesActivated, to_field='name', related_name='+')

    def show(self):
        return "User Service %s %s %s" % (self.user, self.token, self.name)

    def __unicode__(self):
        return "%s" % (self.name)


class TriggerService(models.Model):
    """
    TriggerService
    # Create some Service
    >>> from django.contrib.auth.models import User
    >>> from django_th.models import UserService, TriggerService
    >>> my_user = User.objects.create(id=777,username='foxmask1')
    >>> user1 = User.objects.get(id=777)
    >>> token = ''
    >>> name = 'ServiceRss2'
    >>> status = True
    >>> auth_required = False
    >>> description = 'RSS Feeds Service'
    >>> service_activated = ServicesActivated.objects.create(name=name, status=status, auth_required=auth_required, description=description)
    >>> name = ServicesActivated.objects.get(name='ServiceRss2')
    >>> user_service = UserService.objects.create(user=user1, token=token, name=name)
    >>> token = 'foobar123'
    >>> name = 'ServiceEvernote2'
    >>> status = True
    >>> auth_required = True
    >>> description = 'Evernote Service'
    >>> service_activated = ServicesActivated.objects.create(name=name, status=status, auth_required=auth_required, description=description)
    >>> name = ServicesActivated.objects.get(name='ServiceEvernote2')
    >>> user_service = UserService.objects.create(user=user1, token=token, name=name)
    >>> provider1 = UserService.objects.get(pk=1)
    >>> consummer1 = UserService.objects.get(pk=2)
    >>> date_created1 = '20130610'
    >>> service1 = TriggerService.objects.create(provider=provider1, \
    consummer=consummer1, description="My First Service", user=user1, \
    date_created=date_created1, status=True)

    # Show them
    >>> service1.show()
    'My Service ServiceRss2 ServiceEvernote2 My First Service foxmask1'
    """
    provider = models.ForeignKey(UserService, related_name='+', blank=True)
    consummer = models.ForeignKey(UserService, related_name='+', blank=True)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)
    date_triggered = models.DateTimeField(null=True)
    status = models.BooleanField()

    def show(self):
        return "My Service %s %s %s %s" % (self.provider, self.consummer,
                                           self.description, self.user)

    def __unicode__(self):
        return "%s %s " % (self.provider, self.consummer)


def create_user_profile(sender, instance, created, **kwargs):
    """
        function to create the record in the UserProfile model
    """
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
