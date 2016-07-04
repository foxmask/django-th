#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from django_th.recycle import recycle


class Command(BaseCommand):

    help = 'Trigger all data from cache in version 2'

    def handle(self, *args, **options):
        """
            get all the triggers that need to be handled
        """
        recycle()
