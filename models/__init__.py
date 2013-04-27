# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

#those 2 lines needs to be here to be able to generate the tables
#even if those classes are not used at all
from .evernote import ServiceEvernote
from .rss import ServiceRss


class ServicesActivated(models.Model):
    """
        Services Activated from the admin
    """
    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField()
    auth_required = models.BooleanField()
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    def __unicode__(self):
        return "%s" % (self.name)


class UserProfile(models.Model):
    """
        Related user to handle his profile
    """
    user = models.OneToOneField(User)


class UserService(models.Model):
    """
         UserService a model to link service and user
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    name = models.ForeignKey(
        ServicesActivated, to_field='name', related_name='+')

    def __unicode__(self):
        return "%s" % (self.name)


class TriggerService(models.Model):
    """
        TriggerService

        # Create some Service
        >>> from django.contrib.auth.models import User
        >>> from django_th.models import UserService, TriggerService
        >>> provider1 = UserService.objects.get(pk=1)
        >>> consummer1 = UserService.objects.get(pk=2)
        >>> user1 = User.objects.get(id=1)
        >>> date_created1 = '20130122'
        >>> service1 = TriggerService.objects.create(provider=provider1, \
        consummer=consummer1, description="My First Service", user=user1, \
        date_created=date_created1)

        # Show them
        >>> service1.show()
        'My Service Flux RSS Note Evernote My First Service foxmask 2013-01-23'

    """
    provider = models.ForeignKey(UserService, related_name='+', blank=True)
    consummer = models.ForeignKey(UserService, related_name='+', blank=True)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)

    def show(self):
        return "My Service %s %s %s %s %s" % (self.provider, self.consummer,
                                              self.description, self.user,
                                              self.date_created)

    def __unicode__(self):
        return "%s %s " % (self.provider, self.consummer)


def create_user_profile(sender, instance, created, **kwargs):
    """
        function to create the record in the UserProfile model
    """
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
