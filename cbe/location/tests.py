import os
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.location.models import UrbanPropertyAddress, Country, PoBoxAddress, import_countries


class LocationTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(code="NZL", name="New Zealand")
        self.address = UrbanPropertyAddress.objects.create(street_number_first=1, street_name='Credibility', street_type='Street', locality='Auckland Central', postcode='1022', city='Auckland')
        self.po = PoBoxAddress.objects.create(box_number="123",locality="Space")
        
        with open("test_geo_postal.tsv","w") as f:
            f.write("NZ	1010	Auckland							-36.85	174.765\r\n")
            f.write("NZ	1011	Herne Bay							-36.8447	174.7336\r\n")
            f.write("NZ	1021	Arch Hill							-36.863	174.7432\r\n")

    def tearDown(self):
        os.remove("test_geo_postal.tsv")
        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        self.assertEqual("{}".format(self.country), "New Zealand")
        self.assertEqual("{}".format(self.address), '1 Credibility Street, Auckland Central, Auckland')
        self.assertEqual("{}".format(self.po), 'PO Box 123, Space')


    def test_countries(self):
        """
        Test the country import
        """
        import_countries('NZL|New Zealand|NZ^AFG|Afghanistan|AF')
        self.assertTrue( Country.objects.get(code='NZL').name == 'New Zealand' )
        
        Country.objects.get(code='NZL').country_geo_data("test_geo_postal.tsv")
