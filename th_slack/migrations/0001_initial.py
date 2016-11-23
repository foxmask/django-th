# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slack',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('webhook_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'django_th_slack',
            },
        ),
        migrations.AddField(
            model_name='slack',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]
