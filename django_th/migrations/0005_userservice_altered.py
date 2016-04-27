# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_th', '0004_rss_uuid_remove_uuid_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesactivated',
            name='self_hosted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userservice',
            name='client_id',
            field=models.CharField(blank=True, verbose_name='client id', max_length=255, default=''),
        ),
        migrations.AddField(
            model_name='userservice',
            name='client_secret',
            field=models.CharField(blank=True, verbose_name='client secret', max_length=255, default=''),
        ),
        migrations.AddField(
            model_name='userservice',
            name='host',
            field=models.CharField(blank=True, verbose_name='host', max_length=255, default=''),
        ),
        migrations.AddField(
            model_name='userservice',
            name='password',
            field=models.CharField(blank=True, verbose_name='password', max_length=128, default=''),
        ),
        migrations.AddField(
            model_name='userservice',
            name='username',
            field=models.CharField(blank=True, verbose_name='username', max_length=255, default=''),
        ),
    ]
