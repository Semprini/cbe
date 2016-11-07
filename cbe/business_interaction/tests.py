from django.test import TestCase
#from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.business_interaction.models import BusinessInteraction

class BusinessInteractionTests(TestCase):
    def setUp(self):
        self.interaction = BusinessInteraction.objects.create(description="Test")

        
    def test_state_change(self):
        """
        Check that the state can be saved and checked for changes
        """
        self.interaction.remember_state(BusinessInteraction,fields=('description',),instance=self.interaction)
        self.interaction.description = "Test 2"
        changes=self.interaction.check_state(BusinessInteraction,instance=self.interaction)
        self.assertEqual('{}'.format(changes), "{'description': ('Test', 'Test 2')}")