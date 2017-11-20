
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_th.api.consumer import save_data

from th_slack.models import Slack


@api_view(['POST'])
def slack(request):
    data = {}
    # check that the data are ok with the provided signature
    slack = Slack.objects.filter(slack_token=request.data['token'], team_id=request.data['team_id']).get()
    if slack:
        data['title'] = 'From Slack #{}'.format(request.data['channel_name'])
        data['content'] = request.data['text']
        status = save_data(slack.trigger_id, data)
        return Response({"message": "Success"}) if status else Response({"message": "Bad request"})
    return Response({"message": "Bad request"})
