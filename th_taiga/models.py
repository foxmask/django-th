# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Taiga(Services):
    """
        Model for Taiga Service
    """
    project_name = models.CharField(max_length=50, blank=True)
    webhook_secret_key = models.CharField(max_length=50,
                                          blank=True,
                                          unique=True)

    notify_epic_create = models.BooleanField(default=True)
    notify_epic_change = models.BooleanField(default=True)
    notify_epic_delete = models.BooleanField(default=True)

    notify_relateduserstory_create = models.BooleanField(default=True)
    notify_relateduserstory_delete = models.BooleanField(default=True)

    notify_issue_create = models.BooleanField(default=True)
    notify_issue_change = models.BooleanField(default=True)
    notify_issue_delete = models.BooleanField(default=True)

    notify_userstory_create = models.BooleanField(default=True)
    notify_userstory_change = models.BooleanField(default=True)
    notify_userstory_delete = models.BooleanField(default=True)

    notify_task_create = models.BooleanField(default=True)
    notify_task_change = models.BooleanField(default=True)
    notify_task_delete = models.BooleanField(default=True)

    notify_wikipage_create = models.BooleanField(default=True)
    notify_wikipage_change = models.BooleanField(default=True)
    notify_wikipage_delete = models.BooleanField(default=True)

    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_taiga'

    def show(self):
        """

        :return: string representing object
        """
        return "Services Taiga %s" % self.trigger

    def __str__(self):
        return "%s" % self.trigger
