# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '0006_longer_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggerservice',
            name='date_result',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='result',
            field=models.CharField(default='', max_length=255),
        ),
    ]
