# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instapush',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('app_id', models.URLField(max_length=255)),
                ('app_secret', models.CharField(max_length=255)),
                ('event_name', models.CharField(max_length=255)),
                ('tracker_name', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'django_th_instapush',
            },
        ),
        migrations.AddField(
            model_name='instapush',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]
