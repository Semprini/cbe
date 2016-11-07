from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.location.models import UrbanPropertyAddress, Country


class CustomerTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(code="NZL", name="New Zealand")
        self.address = UrbanPropertyAddress.objects.create(locality='Auckland Central', postcode='1022')

        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        self.assertEqual("{}".format(self.country), "New Zealand")
        self.assertEqual("{}".format(self.address), ', Auckland Central')