
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_th.models import TriggerService
from django_th.services import default_provider

from th_slack.models import Slack


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

    if len(data) > 0:

        getattr(service_consumer, '__init__')(service.consumer.token,
                                              **kwargs)
        status = getattr(service_consumer, 'save_data')(service.id, **data)

    return status


@api_view(['POST'])
def slack(request):
    data = {}
    # check that the data are ok with the provided signature
    slack = Slack.objects.filter(slack_token=request.data['token'],
                                 team_id=request.data['team_id']).get()
    if slack:
        data['title'] = 'From Slack #{}'.format(request.data['channel_name'])
        data['content'] = request.data['text']
        status = consumer(slack.trigger_id, data)
        if status:
            return Response({"message": "Success"})
        else:
            return Response({"message": "Bad request"})
