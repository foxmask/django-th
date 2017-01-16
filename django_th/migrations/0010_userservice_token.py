# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '0009_auto_20161113_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userservice',
            name='token',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
