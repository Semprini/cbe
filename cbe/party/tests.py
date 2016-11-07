from django.test import TestCase
#from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.party.models import Individual, Organisation, TelephoneNumber, EmailContact, GenericPartyRole
from cbe.party.views import IndividualViewSet

class PartyTests(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe", form_of_address='Mr', middle_names='Hubert')
        self.organisation = Organisation.objects.create(name='Pen Inc.')
        self.phone = TelephoneNumber(number="021123456")
        self.email = EmailContact(email_address="test@test.com")
        self.role = GenericPartyRole(party=self.organisation, name="Generic")

        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        john = Individual.objects.get(given_names="John", family_names="Doe")
        self.assertEqual('{}'.format(john), 'Mr John Hubert Doe')
        self.assertEqual('{}'.format(self.organisation), 'Pen Inc.')
        self.assertEqual('{}'.format(self.phone), '021123456')
        self.assertEqual('{}'.format(self.email), 'test@test.com')
        
    def test_role_asignment(self):
        """
        Make sure the party roles can be assigned to individuals and organisations
        """
        self.assertEqual('{}'.format(self.role), 'Pen Inc. as a Generic')
        self.role.individual = self.individual
        self.assertEqual('{}'.format(self.role.party), 'Mr John Hubert Doe')
        self.role.organisation = self.organisation
        self.assertEqual('{}'.format(self.role.party), 'Pen Inc.')

        
class PartyAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.factory = APIRequestFactory()

        
    def test_get_individual(self):
        """
        Test that we can GET the sample Individual
        """
        view = IndividualViewSet.as_view({'get':'list',})
        request = self.factory.get('/party/individual/{}/'.format(self.individual.id),)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        self.assertEqual(response.exception, False)
        
        
    def test_create_individual(self):
        """
        Ensure we can create a new Individual object.
        """
        url = '/api/party/individual/'
        data = {'given_names': 'test first', 'family_names':'test_last'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    def test_putnpatch_individual(self):
        """
        Ensure we can update the Individual.
        """
        url = '/api/party/individual/{}/'.format(self.individual.id)
        data = {'given_names': 'test John', 'family_names':'Doe'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = {'gender': 'Male'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        