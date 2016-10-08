# coding: utf-8
from django.db import models
from django_th.models.services import Services


class Trello(Services):

    """
        Trello model
    """
    # Boards own Lists own Cards

    board_name = models.CharField(max_length=80, blank=False)
    list_name = models.CharField(max_length=80, blank=False)
    card_title = models.CharField(max_length=80)
    card_description = models.CharField(max_length=80, blank=True)
    trigger = models.ForeignKey('TriggerService')

    class Meta:
        app_label = 'django_th'
        db_table = 'django_th_trello'

    def show(self):
        """

        :return: string representing object
        """
        return "My Trello %s %s %s" % (self.board_name,
                                       self.list_name,
                                       self.card_title)

    def __str__(self):
        return "%s %s %s" % (self.board_name,
                             self.list_name,
                             self.card_title)
