import hmac
import hashlib

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_th.api.consumer import save_data

from th_taiga.models import Taiga


class TaigaDomain:

    def factory(type):
        if type == "epic":
            return Epic()
        if type == "issue":
            return Issue()
        if type == "task":
            return Task()
        if type == "userstory":
            return UserStory()
        if type == "wikipage":
            return WikiPage()
        if type == "relateduserstory":
            return RelatedUserStory()
        assert 0, "Bad type creation: " + type

    factory = staticmethod(factory)


class Epic(TaigaDomain):

    def create(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_epic_create:
            data['type_action'] = 'New Epic created'
        return data

    def change(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_epic_change:
            data['type_action'] = 'Changed Epic'
        return data

    def delete(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_epic_delete:
            data['type_action'] = 'Deleted Epic'
        return data


class Issue(TaigaDomain):

    def create(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_issue_create:
            data['type_action'] = 'New Issue created'
        return data

    def change(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_issue_change:
            data['type_action'] = 'Changed Issue'
        return data

    def delete(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_issue_delete:
            data['type_action'] = 'Deleted Issue'
        return data


class UserStory(TaigaDomain):

    def create(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_userstory_create:
            data['type_action'] = 'New Userstory created'

        return data

    def change(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_userstory_change:
            data['type_action'] = 'Changed Userstory'
        return data

    def delete(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_userstory_delete:
            data['type_action'] = 'Deleted Userstory'
        return data


class Task(TaigaDomain):
    def create(self,  taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_task_create:
            data['type_action'] = 'New Task created'
        return data

    def change(self,  taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_task_change:
            data['type_action'] = 'Changed Task'
        return data

    def delete(self,  taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_task_delete:
            data['type_action'] = 'Deleted Task'
        return data


class WikiPage(TaigaDomain):

    def create(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_wikipage_create:
            data['type_action'] = 'New Wikipage created'
        return data

    def change(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_wikipage_change:
            data['type_action'] = 'Changed Wikipage'
        return data

    def delete(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_wikipage_delete:
            data['type_action'] = 'Deleted Wikipage'
        return data


class RelatedUserStory(TaigaDomain):

    def create(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_relateduserstory_create:
            data['type_action'] = 'New Related Userstory created'
        return data

    def delete(self, taiga_obj, data):
        """

        :param taiga_obj: taiga object
        :param data: data to return
        :return: data
        """
        if taiga_obj.notify_relateduserstory_delete:
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

    t = TaigaDomain.factory(domain)
    if action == 'create':
        t.create(taiga_obj, data)
    elif action == 'change':
        t.change(taiga_obj, data)
    elif action == 'delete':
        t.delete(taiga_obj, data)
    return data


def verify_signature(data, key, signature):
    mac = hmac.new(key.encode("utf-8"), msg=data, digestmod=hashlib.sha1)
    return mac.hexdigest() == signature


@api_view(['POST'])
def taiga(request, trigger_id, key):
    signature = request.META.get('HTTP_X_TAIGA_WEBHOOK_SIGNATURE')
    # check that the data are ok with the provided signature
    if verify_signature(request._request.body, key, signature):
        data = data_filter(trigger_id, **request.data)
        status = save_data(trigger_id, data)
        return Response({"message": "Success"}) if status else Response({"message": "Failed!"})
    Response({"message": "Bad request"})
