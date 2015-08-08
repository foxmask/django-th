# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rss',
            name='uuid',
            field=models.UUIDField(editable=False, null=True, default=uuid.uuid4),
        ),
    ]
