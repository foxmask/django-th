#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import arrow

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django_th.models import Digest


class Command(BaseCommand):

    help = 'Trigger all data from cache in version 2'

    def handle(self, *args, **options):
        """
            get all the digest data to send to each user
        """
        now = arrow.utcnow().to(settings.TIME_ZONE)
        now = now.date()

        digest = Digest.objects.filter(date_end=str(now)).order_by('user', 'date_end')
        users = digest.distinct('user')

        subject = 'Your digester'

        msg_plain = render_to_string('digest/email.txt', {'digest': digest, 'subject': subject})
        msg_html = render_to_string('digest/email.html', {'digest': digest, 'subject': subject})
        message = msg_plain
        from_email = settings.ADMINS
        recipient_list = ()
        for user in users:
            recipient_list += (user.user.email,)

        send_mail(subject, message, from_email, recipient_list,
                  html_message=msg_html)
