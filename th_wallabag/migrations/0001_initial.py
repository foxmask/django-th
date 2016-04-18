# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallabag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=80, blank=True)),
                ('url', models.URLField(max_length=255)),
                ('title', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'db_table': 'django_th_wallabag',
            },
        ),
        migrations.AddField(
            model_name='wallabag',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]