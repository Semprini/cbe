from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.party.models import Individual, Organisation
from cbe.physical_object.models import Vehicle, Structure, Owner
from cbe.physical_object.views import OwnerViewSet

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


class OwnerAPITests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.individual = Individual.objects.create(
            given_names="John", family_names="Doe")
        self.organisation = Organisation.objects.create(name='Pen Inc.')
        self.owner = Owner.objects.create(
            party=self.individual, )
        self.factory = APIRequestFactory()

    def test_get_owner(self):
        """
        Test that we can GET the sample Owner
        """
        view = OwnerViewSet.as_view({'get': 'list', })
        request = self.factory.get(
            '/physical_object/owner/{}/'.format(self.owner.pk),)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        self.assertEqual(response.exception, False)

    def test_create_owner(self):
        """
        Ensure we can create a new Owner object.
        """
        url = '/api/physical_object/owner/'
        data = {
            "party": {
                "type": "Individual",
                "url": "http://127.0.0.1:8000/api/party/individual/{}/".format(self.individual.pk),
                'given_names': 'Bob'},
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "party": {
                "type": "Organisation",
                "url": "http://127.0.0.1:8000/api/party/organisation/{}/".format(self.organisation.pk)},
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        