# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# from .lib import *


class TriggerType(models.Model):
    """
        TriggerType to store the Type of Service

        the code is the name of the provider/consumer located in dir .lib/

        # Create some Type
        >>> rss = TriggerType.objects.create(name="RSS Feeds", code="RSS")
        >>> evernote = TriggerType.objects.create(name="Evernote Note", \
        code="Evernote")

        # Show them
        >>> rss.show()
        'My Service Type RSS named RSS Feeds'
        >>> evernote.show()
        'My Service Type Evernote named Evernote Note'
    """
    code = models.CharField(max_length=80, primary_key=True)
    name = models.CharField(max_length=140)

    def __unicode__(self):
        """
            required to build the drop down list
            otherwise will dislpay <TriggerType object>
        """
        return "%s" % (self.name)

    def show(self):
        return "My Service Type %s named %s" % (self.code, self.name)


class TriggerService(models.Model):
    """
        TriggerService

        # Create some Service
        >>> from django.contrib.auth.models import User
        >>> from django_th.models import TriggerType, TriggerService
        >>> provider1 = TriggerType.objects.get(pk=1)
        >>> consummer1 = TriggerType.objects.get(pk=2)
        >>> user1 = User.objects.get(id=1)
        >>> date_created1 = '20130122'
        >>> service1 = TriggerService.objects.create(provider=provider1, \
        consummer=consummer1, description="My First Service", user=user1, \
        date_created=date_created1)

        # Show them
        >>> service1.show()
        'My Service Flux RSS Note Evernote My First Service foxmask 2013-01-23'

    """
    provider = models.ForeignKey(TriggerType, related_name='+', blank=True)
    consummer = models.ForeignKey(TriggerType, related_name='+', blank=True)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)

    def show(self):
        return "My Service %s %s %s %s %s" % (self.provider, self.consummer,
                                              self.description, self.user,
                                              self.date_created)


class UserService(models.Model):
    """
        UserService a model to link service and user
    """
    user = models.ForeignKey(User)
    code = models.ForeignKey(TriggerType, related_name='+')


class UserProfile(models.Model):
    """
        Related user to handle his profile
    """
    user = models.OneToOneField(User)


def create_user_profile(sender, instance, created, **kwargs):
    """
        function to create the record in the UserProfile model
    """
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
