# coding: utf-8

from django import forms
from th_taiga.models import Taiga


class TaigaForm(forms.ModelForm):

    """
        form to handle Slack service
    """

    class Meta:
        model = Taiga
        fields = ('project_name',
                  'webhook_secret_key',
                  'notify_epic_create',
                  'notify_epic_change',
                  'notify_epic_delete',
                  'notify_relateduserstory_create',
                  'notify_relateduserstory_delete',
                  'notify_issue_create',
                  'notify_issue_change',
                  'notify_issue_delete',
                  'notify_userstory_create',
                  'notify_userstory_change',
                  'notify_userstory_delete',
                  'notify_task_create',
                  'notify_task_change',
                  'notify_task_delete',
                  'notify_wikipage_create',
                  'notify_wikipage_change',
                  'notify_wikipage_delete')


class TaigaProviderForm(TaigaForm):
    pass


class TaigaConsumerForm(TaigaForm):
    pass
