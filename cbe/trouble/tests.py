from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.trouble.models import TroubleTicket, TroubleTicketItem

class TroubleTests(TestCase):
    def setUp(self):
        self.trouble = TroubleTicket.objects.create(trouble_ticket_state="New", description="Test")
        self.item = TroubleTicketItem.objects.create( business_interaction=self.trouble, action="Test Item" )

    def test_names(self):
        """
        Check that the trouble names display as expected
        """
        name = '{}'.format(self.trouble)
        self.assertEqual(name.split(':')[0], "New")
        self.assertEqual('{}'.format(self.item).split(':')[5], "Test Item")
