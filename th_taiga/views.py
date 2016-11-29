import hmac
import hashlib

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_th.models import TriggerService
from django_th.services import default_provider

from th_taiga.models import Taiga


def data_filter(trigger_id, **data):
    """
    check if we want to track event for a given action
    :param trigger_id:
    :param data:
    :return:
    """
    taiga = Taiga.objects.get(trigger_id=trigger_id)

    action = data.get('action')
    type = data.get('type')
    data = data.get('data')

    if type == 'epic' and action == 'create' and taiga.notify_epic_create:
        data['type_action'] = 'New Epic created'
    elif type == 'epic' and action == 'change' and taiga.notify_epic_change:
        data['type_action'] = 'Changed Epic'
    elif type == 'epic' and action == 'delete' and taiga.notify_epic_delete:
        data['type_action'] = 'Deleted Epic'
    elif type == 'issue' and action == 'create' and \
            taiga.notify_issue_create:
        data['type_action'] = 'New Issue created'
    elif type == 'issue' and action == 'change' and \
            taiga.notify_issue_change:
        data['type_action'] = 'Changed Issue'
    elif type == 'issue' and action == 'delete' and \
            taiga.notify_issue_delete:
        data['type_action'] = 'Deleted Issue'
    elif type == 'userstory' and action == 'create' and \
            taiga.notify_userstory_create:
        data['type_action'] = 'New Userstory created'
    elif type == 'userstory' and action == 'change' and \
            taiga.notify_userstory_change:
        data['type_action'] = 'Changed Userstory'
    elif type == 'userstory' and action == 'delete' and \
            taiga.notify_userstory_delete:
        data['type_action'] = 'Deleted Userstory'
    elif type == 'task' and action == 'create' and \
            taiga.notify_task_create:
        data['type_action'] = 'New Task created'
    elif type == 'task' and action == 'change' and \
            taiga.notify_task_change:
        data['type_action'] = 'Changed Task'
    elif type == 'task' and action == 'delete' and \
            taiga.notify_task_delete:
        data['type_action'] = 'Deleted Task'
    elif type == 'wikipage' and action == 'create' and \
            taiga.notify_wikipage_create:
        data['type_action'] = 'New Wikipage created'
    elif type == 'wikipage' and action == 'change' and \
            taiga.notify_wikipage_change:
        data['type_action'] = 'Changed Wikipage'
    elif type == 'wikipage' and action == 'delete' and \
            taiga.notify_wikipage_delete:
        data['type_action'] = 'Deleted Wikipage'
    elif type == 'relateduserstory' and action == 'create' and \
            taiga.notify_relateduserstory_create:
        data['type_action'] = 'New Related Userstory created'
    elif type == 'relateduserstory' and action == 'delete' and \
            taiga.notify_relateduserstory_delete:
        data['type_action'] = 'Deleted Related Userstory'
    else:
        data = []

    return data


def consumer(trigger_id, data):
    """
        call the consumer and handle the data
        :param trigger_id:
        :param data:
        :return:
    """
    # consumer - the service which uses the data
    default_provider.load_services()
    service = TriggerService.objects.get(id=trigger_id)

    service_consumer = default_provider.get_service(
        str(service.consumer.name.name))
    kwargs = {'user': service.user}

    data = data_filter(trigger_id, **data)
    if len(data) > 0:

        getattr(service_consumer, '__init__')(service.consumer.token,
                                              **kwargs)
        getattr(service_consumer, 'save_data')(service.id, **data)


def verify_signature(data, key, signature):
    mac = hmac.new(key.encode("utf-8"), msg=data, digestmod=hashlib.sha1)
    return mac.hexdigest() == signature


@api_view(['POST'])
def taiga(request, trigger_id, key):
    signature = request.META.get('HTTP_X_TAIGA_WEBHOOK_SIGNATURE')
    # check that the data are ok with the provided signature
    if verify_signature(request._request.body, key, signature):
        consumer(trigger_id, request.data)
        return Response({"message": "Success"})
    else:
        return Response({"message": "Failed!"})
