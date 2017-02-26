from django.test import TestCase
#from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem, BusinessInteractionRole


# class BusinessInteractionTests(TestCase):

    # def setUp(self):
        # self.role = BusinessInteractionRole.objects.create(
            # business_interaction=self.interaction, 
            # name="Test Role")

    # def test_names(self):
        # """
        # Check that the names display as expected
        # """
        # name = '{}'.format(self.role)
        # self.assertEqual(name, "None involved in None as a Test Role")
        # self.assertEqual('{}'.format(self.item).split(':')[5], "Test Item")
        # self.assertEqual(
           # '{}'.format(self.role).split(':')[4], "Test at None as a Test Role")

    # def test_state_change(self):
        # """
        # Check that the state can be saved and checked for changes
        # """
        # self.interaction.remember_state(
            # BusinessInteraction, fields=('description',), instance=self.interaction)
        # self.interaction.description = "Test 2"
        # changes = self.interaction.check_state(
            # BusinessInteraction, instance=self.interaction)
        # self.assertEqual(
            # '{}'.format(changes), "{'description': ('Test', 'Test 2')}")
