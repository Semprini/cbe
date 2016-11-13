from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.trouble.models import TroubleTicket, TroubleTicketItem, TROUBLE_TICKET_CHOICES,Problem,ResourceAlarm,TrackingRecord

class TroubleTests(TestCase):
    def setUp(self):
        self.trouble = TroubleTicket.objects.create(trouble_ticket_state=TROUBLE_TICKET_CHOICES[0][0], description="Test")
        self.item = TroubleTicketItem.objects.create( trouble_ticket=self.trouble, business_interaction=self.trouble, action="Test Item" )
        self.problem = Problem.objects.create(originatingSytem='Test System',description='Test desc',reason='Test reason')
        self.alarm = ResourceAlarm.objects.create(alarmType='Test Alarm', specificProblem=self.problem)
        self.tracking = TrackingRecord.objects.create(problem=self.problem, system='Test System')

    def test_names(self):
        """
        Check that the trouble names display as expected
        """
        self.assertEqual('{}'.format(self.trouble.__str__()).split(':')[0], "Queued")
        self.assertTrue( self.trouble.trouble_detection_date )
        self.assertEqual('{}'.format(self.item.__str__()).split(':')[5], "Test Item")

        self.assertEqual('{}'.format(self.alarm), "1:Test Alarm")
        self.assertEqual('{}'.format(self.problem).split(':')[0], 'Test System')
        self.assertEqual('{}'.format(self.tracking).split(':')[0:2], ["1","Test System"])
