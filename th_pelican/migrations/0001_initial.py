# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pelican',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=80)),
                ('url', models.URLField()),
                ('tags', models.CharField(blank=True, max_length=200)),
                ('category', models.CharField(blank=True, max_length=200)),
                ('path', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'django_th_pelican',
            },
        ),
        migrations.AddField(
            model_name='pelican',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]
