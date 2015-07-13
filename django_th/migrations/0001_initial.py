# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Pocket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=80, blank=True)),
                ('url', models.URLField(max_length=255)),
                ('title', models.CharField(max_length=80, blank=True)),
                ('tweet_id', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'db_table': 'django_th_pocket',
            },
        ),
        migrations.CreateModel(
            name='Rss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
            ],
            options={
                'db_table': 'django_th_rss',
            },
        ),
        migrations.CreateModel(
            name='ServicesActivated',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('status', models.BooleanField(default=False)),
                ('auth_required', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Services',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='TriggerService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_triggered', models.DateTimeField(null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=80, blank=True, null=True)),
                ('screen', models.CharField(max_length=80, blank=True, null=True)),
                ('since_id', models.BigIntegerField(blank=True, null=True)),
                ('max_id', models.BigIntegerField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('trigger', models.ForeignKey(to='django_th.TriggerService')),
            ],
            options={
                'db_table': 'django_th_twitter',
            },
        ),
        migrations.CreateModel(
            name='UserService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('name', models.ForeignKey(to_field='name', to='django_th.ServicesActivated', related_name='+')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='consumer',
            field=models.ForeignKey(blank=True, related_name='+', to='django_th.UserService'),
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='provider',
            field=models.ForeignKey(blank=True, related_name='+', to='django_th.UserService'),
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rss',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
        migrations.AddField(
            model_name='pocket',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
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
        migrations.AddField(
            model_name='evernote',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]
