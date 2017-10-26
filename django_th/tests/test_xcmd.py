# coding: utf-8
from django.core import management


from django.test import TestCase


class TestCmdMgt(TestCase):

    def test_run(self):
        management.call_command('recycle', verbosity=0, interactive=False)
        management.call_command('read', verbosity=0, interactive=False)
        management.call_command('publish', verbosity=0, interactive=False)
        management.call_command('read_n_pub', trigger_id=1, verbosity=0, interactive=False)
        # management.call_command('send_digest', verbosity=0, interactive=False)
