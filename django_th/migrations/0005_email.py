# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '0004_rss_uuid_remove_uuid_null'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('trigger', models.ForeignKey(to='django_th.TriggerService')),
            ],
            options={
                'db_table': 'django_th_email',
            },
        ),
    ]
