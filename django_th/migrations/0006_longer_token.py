# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_th', '0005_userservice_altered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userservice',
            name='token',
            field=models.CharField(max_length=1024),
        ),
    ]
