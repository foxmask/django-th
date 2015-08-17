# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evernote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=80, blank=True)),
                ('notebook', models.CharField(max_length=80)),
                ('title', models.CharField(max_length=80)),
                ('text', models.TextField()),
            ],
            options={
                'db_table': 'django_th_evernote',
            },
        ),
        migrations.AddField(
            model_name='evernote',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]
