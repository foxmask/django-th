# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('th_twitter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter',
            name='max_id',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twitter',
            name='since_id',
            field=models.BigIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
