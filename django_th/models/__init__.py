# coding: utf-8
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ServicesActivated(models.Model):
    """
        Services Activated from the admin
    """
    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField(default=False)
    auth_required = models.BooleanField(default=True)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    def show(self):
        return "Service Activated %s %s %s %s" % (self.name, self.status,
                                                  self.auth_required, self.description)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """
        Related user to handle his profile
    """
    user = models.OneToOneField(User)

    def show(self):
        return "User profile %s" % (self.user_id)

    def __str__(self):
        return "%s" % (self.user)


@python_2_unicode_compatible
class UserService(models.Model):
    """
        UserService a model to link service and user
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    name = models.ForeignKey(
        ServicesActivated, to_field='name', related_name='+')

    def show(self):
        return "User Service %s %s %s" % (self.user, self.token, self.name)

    def __str__(self):
        return "%s" % (self.name)


@python_2_unicode_compatible
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

    def show(self):
        return "My Service %s %s %s %s" % (self.provider, self.consumer, self.description, self.user)

    def __str__(self):
        return "%s %s " % (self.provider, self.consumer)


def create_user_profile(sender, instance, created, **kwargs):
    """
        function to create the record in the UserProfile model
    """
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
