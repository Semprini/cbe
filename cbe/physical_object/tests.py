from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.party.models import Individual, Organisation
from cbe.physical_object.models import Vehicle, Structure


class MockRequest(object):
    pass


class MockSuperUser(object):

    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class VehicleTestCase(TestCase):

    def setUp(self):
        o = Organisation.objects.create( name="Toyota" )
        self.vehicle = Vehicle.objects.create(
            make=o, series="Camry", model="Sportivo" )

    def test_names(self):
        """
        Make sure the names display as expected
        """
        v = Vehicle.objects.get(id=self.vehicle.id)
        self.assertEqual("{}".format(v), 'Toyota Camry Sportivo')

        
class StructureTestCase(TestCase):

    def setUp(self):
        o = Organisation.objects.create( name="Bobs Buildings" )
        self.structure = Structure.objects.create(
            make=o )

    def test_names(self):
        """
        Make sure the names display as expected
        """
        s = Structure.objects.get(id=self.structure.id)
        self.assertEqual("{}".format(s), 'Structure by Bobs Buildings')


     