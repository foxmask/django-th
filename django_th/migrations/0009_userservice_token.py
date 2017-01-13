# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '0008_update_date_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userservice',
            name='token',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
