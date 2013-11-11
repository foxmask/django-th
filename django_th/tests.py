import unittest
from django.test import RequestFactory
from django_th.views import TriggerEditedTemplateView, TriggerDeletedTemplateView, UserServiceAddedTemplateView, UserServiceDeletedTemplateView



class TriggerEditedTemplateViewTestCase(unittest.TestCase):

        def test_get(self):

                template_name = "triggers/thanks_trigger.html"
                # Setup request and view.
                request = RequestFactory().get('/trigger/edit/thanks')
                view = TriggerEditedTemplateView.as_view(template_name=template_name)
                sentance = 'Your trigger has been successfully modified'
                # Run.
                response = view(request)
                # Check.
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.template_name[0], 'triggers/thanks_trigger.html')
                self.assertEqual(response.context_data['sentance'], sentance)        


class TriggerDeletedTemplateViewTestCase(unittest.TestCase):

        def test_get(self):

                template_name = "triggers/thanks_trigger.html"
                # Setup request and view.
                request = RequestFactory().get('/trigger/delete/thanks')
                view = TriggerDeletedTemplateView.as_view(template_name=template_name)
                sentance = 'Your trigger has been successfully deleted'
                # Run.
                response = view(request)
                # Check.
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.template_name[0], 'triggers/thanks_trigger.html')
                self.assertEqual(response.context_data['sentance'], sentance)      


class UserServiceAddedTemplateViewTestCase(unittest.TestCase):

        def test_get(self):
                template_name = 'services/thanks_service.html'
                # Setup request and view.
                request = RequestFactory().get('/service/add/thanks')
                view = UserServiceAddedTemplateView.as_view(template_name=template_name)
                sentance = 'Your service has been successfully created'
                # Run.
                response = view(request)
                # Check.
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.template_name[0], 'services/thanks_service.html')
                self.assertEqual(response.context_data['sentance'], sentance)                    


class UserServiceDeletedTemplateViewTestCase(unittest.TestCase):

        def test_get(self):
                template_name = 'services/thanks_service.html'
                # Setup request and view.
                request = RequestFactory().get('/service/delete/thanks')
                view = UserServiceDeletedTemplateView.as_view(template_name=template_name)
                sentance = 'Your service has been successfully deleted'
                # Run.
                response = view(request)
                # Check.
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.template_name[0], 'services/thanks_service.html')
                self.assertEqual(response.context_data['sentance'], sentance)

