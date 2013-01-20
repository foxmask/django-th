# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
# from .lib import *


class TriggerType(models.Model):
    """
        TriggerType

        the code is the name of the provider/consumer located in dir .lib/
    """
    code = models.CharField(max_length=80)
    name = models.CharField(max_length=140)

    def __unicode__(self):
        """
            required to build the drop down list
            otherwise will dislpay <TriggerType object>
        """
        return "%s" % (self.name)


class TriggerService(models.Model):
    """
        TriggerService
    """
    provider = models.ForeignKey(TriggerType, related_name='+', blank=True)
    consummer = models.ForeignKey(TriggerType, related_name='+', blank=True)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)


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
