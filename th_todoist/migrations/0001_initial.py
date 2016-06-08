# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_th', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todoist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'django_th_todoist',
            },
        ),
        migrations.AddField(
            model_name='todoist',
            name='trigger',
            field=models.ForeignKey(to='django_th.TriggerService'),
        ),
    ]