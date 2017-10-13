# coding: utf-8
import arrow
import datetime
from django.test import TestCase

from django_th.tools import class_for_name, get_service, to_datetime,\
    download_image
from django_th.html_entities import HtmlEntities


class ToolsTest(TestCase):

    def test_class_for_name(self):
        service_name = 'Twitter'
        form_name = service_name + 'ProviderForm'
        class_name = 'th_' + service_name.lower() + '.forms'
        form_class = class_for_name(class_name, form_name)
        self.assertTrue(form_class, 'TwitterFormProvider')

    def test_get_service(self):
        my_service = 'ServiceTwitter'
        model = get_service(my_service)
        self.assertTrue(model, 'Twitter')

        my_service = 'ServiceTwitter'
        form = get_service(my_service, 'forms')
        self.assertTrue(form, 'TwitterProviderForm')

    def test_to_datetime(self):
        now = arrow.utcnow().to('Europe/Paris').timetuple()
        data = {'published_parsed': now}
        date = to_datetime(data)
        self.assertTrue(type(date), type(datetime))
        data = {'created_parsed': now}
        date = to_datetime(data)
        self.assertTrue(type(date), type(datetime))
        data = {'updated_parsed': now}
        date = to_datetime(data)
        self.assertTrue(type(date), type(datetime))
        data = {'my_date': now}
        date = to_datetime(data)
        self.assertTrue(type(date), type(datetime))

    def test_download_image(self):
        url = 'https://foxmask.trigger-happy.eu/static/ouaf.jpg'
        local_filename = download_image(url)
        self.assertTrue(type(str), local_filename)


class HtmlEntitiesTest(TestCase):

    def test_html_entity_decode(self):
        my_string = "&#62;"
        my_string = HtmlEntities(my_string).html_entity_decode
        self.assertTrue(my_string, str)
