import hmac
import hashlib

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_th.models import TriggerService
from django_th.services import default_provider


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
    getattr(service_consumer, '__init__')(service.consumer.token,
                                          **kwargs)
    data = data.get('data')
    data['link'] = data.get('permalink')
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
