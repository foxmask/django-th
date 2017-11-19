from django_th.models import TriggerService
from django_th.services import default_provider


def save_data(trigger_id, data):
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

    service_consumer = default_provider.get_service(str(service.consumer.name.name))
    kwargs = {'user': service.user}

    if len(data) > 0:
        getattr(service_consumer, '__init__')(service.consumer.token, **kwargs)
        status = getattr(service_consumer, 'save_data')(service.id, **data)

    return status
