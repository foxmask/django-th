from django_th.models import TriggerService

from oauth2_provider.decorators import rw_protected_resource

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from th_twitter.my_twitter import ServiceTwitter

# 1- oAuth protection
# 2- then check the data


@rw_protected_resource()
@api_view(['POST'])
def tweet(request):
    """
    before tweeting, oAuth will check the token to access to TriggerHappy API
    then will check the post'ing data
    then will create the tweet
    :param request:
    :return:
    """
    data = {}

    if 'link' in request.data\
            and 'title' in request.data\
            and 'content' in request.data:

        try:
            trigger = TriggerService.objects.filter(
                user=request.data['user'],
                trigger_id=request.data['id'],
                consumer='ServiceTwitter'
            )
        except TriggerService.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if trigger:
            data['link'] = request.data['link']
            data['title'] = request.data['title']
            data['content'] = request.data['content']
            twitter = ServiceTwitter(token=trigger.consumer.token,
                                     trigger_id=request.data['id'])
            result = twitter.save_data(request.data['id'], **data)

            if result:
                return Response(data, status=status.HTTP_201_CREATED)

    return Response({"message": "Bad request"},
                    status=status.HTTP_400_BAD_REQUEST)
