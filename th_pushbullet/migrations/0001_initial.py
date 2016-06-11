# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pushbullet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=4)),
                ('device', models.CharField(max_length=80, blank=True)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('channel_tag', models.CharField(max_length=80, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'django_th_pushbullet',
            },
        ),
        migrations.AddField(
            model_name='pushbullet',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]