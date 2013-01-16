# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save


class TriggerHappyType(models.Model):
    """
        TriggerHappyType
    """
    name = models.CharField(max_length=140)



class TriggerHappy(models.Model):
    """
        TriggerHappy
    """
    name = models.CharField(max_length=140)
    trigger_type = models.ForeignKey(TriggerHappyType)
    user = models.ForeignKey(User)
    date_created = models.DateField()


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

