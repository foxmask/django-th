# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tumblr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('blogname', models.CharField(max_length=80)),
                ('tag', models.CharField(blank=True, max_length=80)),
                ('trigger', models.ForeignKey(to='django_th.TriggerService')),
            ],
            options={
                'db_table': 'django_th_tumblr',
            },
        ),
    ]
