# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    """
        this migration will be used to add 2 field to deal with
        things that will go wrong that will then trigger
        mail to admin and author of the triggers
    """

    dependencies = [
        ('django_th', '0008_update_date_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='triggerservice',
            name='consumer_failed',
            field=models.IntegerField(default=0, db_index=True),
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='provider_failed',
            field=models.IntegerField(default=0, db_index=True),
        ),
    ]
