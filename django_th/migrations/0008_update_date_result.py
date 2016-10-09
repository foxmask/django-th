# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def update_date_result(apps, schema):
    TriggerService = apps.get_model("django_th", "TriggerService")
    for trigger in TriggerService.objects.all():
        trigger.date_result = trigger.date_triggered
        trigger.result = 'OK'
        trigger.save()


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '0007_trigger_result'),
    ]
    operations = [
        migrations.RunPython(update_date_result),
    ]
