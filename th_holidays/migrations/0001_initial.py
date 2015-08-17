# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('status', models.BooleanField()),
            ],
            options={
                'db_table': 'django_th_holidays',
            },
        ),
        migrations.AddField(
            model_name='holidays',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
        migrations.AddField(
            model_name='holidays',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
