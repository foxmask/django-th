# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=80, null=True, blank=True)),
                ('screen', models.CharField(max_length=80, null=True, blank=True)),
                ('since_id', models.IntegerField(null=True, blank=True)),
                ('max_id', models.IntegerField(null=True, blank=True)),
                ('count', models.IntegerField(null=True, blank=True)),
                ('trigger', models.ForeignKey(to='django_th.TriggerService')),
            ],
            options={
                'db_table': 'django_th_twitter',
            },
            bases=(models.Model,),
        ),
    ]
