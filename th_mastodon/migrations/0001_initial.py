# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mastodon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('timeline', models.CharField(choices=[('home', 'Home'), ('public', 'Public')], default='home', max_length=10)),
                ('tooter', models.CharField(blank=True, max_length=80, null=True)),
                ('fav', models.BooleanField(default=False)),
                ('tag', models.CharField(blank=True, max_length=80, null=True)),
                ('since_id', models.BigIntegerField(blank=True, null=True)),
                ('max_id', models.BigIntegerField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'django_th_mastodon',
            },

        ),
        migrations.AddField(
            model_name='mastodon',
            name='trigger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_th.TriggerService'),
        ),
    ]
