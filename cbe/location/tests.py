from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.location.models import UrbanPropertyAddress, Country, PoBoxAddress


class LocationTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(code="NZL", name="New Zealand")
        self.address = UrbanPropertyAddress.objects.create(street_number_first=1, street_name='Credibility', street_type='Street', locality='Auckland Central', postcode='1022', city='Auckland')
        self.po = PoBoxAddress.objects.create(box_number="123",locality="Space")

        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        self.assertEqual("{}".format(self.country), "New Zealand")
        self.assertEqual("{}".format(self.address), '1 Credibility Street, Auckland Central, Auckland')
        self.assertEqual("{}".format(self.po), 'PO Box 123, Space')