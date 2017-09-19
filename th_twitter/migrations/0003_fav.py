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
        ('th_twitter', '0002_int_to_bigint'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter',
            name='fav',
            field=models.BooleanField(default=0),
        ),
    ]
