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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('project_name', models.CharField(max_length=50, blank=True)),
                ('webhook_secret_key', models.CharField(max_length=50, unique=True, blank=True)),
                ('notify_epic_create', models.BooleanField(default=True)),
                ('notify_epic_change', models.BooleanField(default=True)),
                ('notify_epic_delete', models.BooleanField(default=True)),
                ('notify_relateduserstory_create', models.BooleanField(default=True)),
                ('notify_relateduserstory_delete', models.BooleanField(default=True)),
                ('notify_issue_create', models.BooleanField(default=True)),
                ('notify_issue_change', models.BooleanField(default=True)),
                ('notify_issue_delete', models.BooleanField(default=True)),
                ('notify_userstory_create', models.BooleanField(default=True)),
                ('notify_userstory_change', models.BooleanField(default=True)),
                ('notify_userstory_delete', models.BooleanField(default=True)),
                ('notify_task_create', models.BooleanField(default=True)),
                ('notify_task_change', models.BooleanField(default=True)),
                ('notify_task_delete', models.BooleanField(default=True)),
                ('notify_wikipage_create', models.BooleanField(default=True)),
                ('notify_wikipage_change', models.BooleanField(default=True)),
                ('notify_wikipage_delete', models.BooleanField(default=True)),
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


