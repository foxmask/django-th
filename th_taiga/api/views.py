import hmac
import hashlib

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_th.models import TriggerService
from django_th.services import default_provider

from th_taiga.models import Taiga


def epic(taiga_obj, action, data):
    """

    :param taiga_obj: taiga object
    :param action: craete/change/delete
    :param data: data to return
    :return: data
    """
    if action == 'create' and taiga_obj.notify_epic_create:
        data['type_action'] = 'New Epic created'
    elif action == 'change' and taiga_obj.notify_epic_change:
        data['type_action'] = 'Changed Epic'
    elif action == 'delete' and taiga_obj.notify_epic_delete:
        data['type_action'] = 'Deleted Epic'
    return data


def issue(taiga_obj, action, data):
    """

    :param taiga_obj: taiga object
    :param action: craete/change/delete
    :param data: data to return
    :return: data
    """
    if action == 'create' and taiga_obj.notify_issue_create:
        data['type_action'] = 'New Issue created'
    elif action == 'change' and taiga_obj.notify_issue_change:
        data['type_action'] = 'Changed Issue'
    elif action == 'delete' and taiga_obj.notify_issue_delete:
        data['type_action'] = 'Deleted Issue'
    return data


def userstory(taiga_obj, action, data):
    """

    :param taiga_obj: taiga object
    :param action: craete/change/delete
    :param data: data to return
    :return: data
    """
    if action == 'create' and taiga_obj.notify_userstory_create:
        data['type_action'] = 'New Userstory created'
    elif action == 'change' and taiga_obj.notify_userstory_change:
        data['type_action'] = 'Changed Userstory'
    elif action == 'delete' and taiga_obj.notify_userstory_delete:
        data['type_action'] = 'Deleted Userstory'
    return data


def task(taiga_obj, action, data):
    """

    :param taiga_obj: taiga object
    :param action: craete/change/delete
    :param data: data to return
    :return: data
    """
    if action == 'create' and taiga_obj.notify_task_create:
        data['type_action'] = 'New Task created'
    elif action == 'change' and taiga_obj.notify_task_change:
        data['type_action'] = 'Changed Task'
    elif action == 'delete' and taiga_obj.notify_task_delete:
        data['type_action'] = 'Deleted Task'
    return data


def wikipage(taiga_obj, action, data):
    """

    :param taiga_obj: taiga object
    :param action: craete/change/delete
    :param data: data to return
    :return: data
    """
    if action == 'create' and taiga_obj.notify_wikipage_create:
        data['type_action'] = 'New Wikipage created'
    elif action == 'change' and taiga_obj.notify_wikipage_change:
        data['type_action'] = 'Changed Wikipage'
    elif action == 'delete' and taiga_obj.notify_wikipage_delete:
        data['type_action'] = 'Deleted Wikipage'
    return data


def relateduserstory(taiga_obj, action, data):
    """

    :param taiga_obj: taiga object
    :param action: craete/change/delete
    :param data: data to return
    :return: data
    """
    if action == 'create' and taiga_obj.notify_relateduserstory_create:
        data['type_action'] = 'New Related Userstory created'
    elif action == 'delete' and taiga_obj.notify_relateduserstory_delete:
        data['type_action'] = 'Deleted Related Userstory'
    return data


def data_filter(trigger_id, **data):
    """
    check if we want to track event for a given action
    :param trigger_id:
    :param data:
    :return:
    """
    taiga_obj = Taiga.objects.get(trigger_id=trigger_id)

    action = data.get('action')
    domain = data.get('type')
    data = data.get('data')

    if domain == 'epic':
        data = epic(taiga_obj, action, data)
    elif domain == 'issue':
        data = issue(taiga_obj, action, data)
    elif domain == 'userstory':
        data = userstory(taiga_obj, action, data)
    elif domain == 'task':
        data = task(taiga_obj, action, data)
    elif domain == 'wikipage':
        data = wikipage(taiga_obj, action, data)
    elif domain == 'relateduserstory':
        data = relateduserstory(taiga_obj, action, data)
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
    status = True
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
        status = getattr(service_consumer, 'save_data')(service.id, **data)

    return status


def verify_signature(data, key, signature):
    mac = hmac.new(key.encode("utf-8"), msg=data, digestmod=hashlib.sha1)
    return mac.hexdigest() == signature


@api_view(['POST'])
def taiga(request, trigger_id, key):
    signature = request.META.get('HTTP_X_TAIGA_WEBHOOK_SIGNATURE')
    # check that the data are ok with the provided signature
    if verify_signature(request._request.body, key, signature):
        status = consumer(trigger_id, request.data)
        if status:
            return Response({"message": "Success"})
        else:
            return Response({"message": "Failed!"})
