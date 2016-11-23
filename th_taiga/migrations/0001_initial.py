# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taiga',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=50)),
                ('webhook_secret_key', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'django_th_taiga',
            },
        ),
        migrations.AddField(
            model_name='taiga',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]
