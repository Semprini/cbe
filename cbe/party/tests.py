from django.test import TestCase
#from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib.admin.options import ( HORIZONTAL, VERTICAL, ModelAdmin, TabularInline, )
from django.contrib.admin.sites import AdminSite
from django.core.checks import Error
from django.forms.models import BaseModelFormSet
from django.forms.widgets import Select
from django.test import SimpleTestCase, TestCase
from django.utils import six

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.party.models import Individual, Organisation, TelephoneNumber, EmailContact, GenericPartyRole
from cbe.party.views import IndividualViewSet
from cbe.party.admin import GenericPartyRoleAdminForm, GenericPartyRoleAdmin

class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()

class PartyTests(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe", form_of_address='Mr', middle_names='Hubert')
        self.organisation = Organisation.objects.create(name='Pen Inc.')
        self.phone = TelephoneNumber.objects.create(number="021123456")
        self.email = EmailContact.objects.create(email_address="test@test.com")
        self.role = GenericPartyRole.objects.create(party=self.organisation, name="Generic")

        
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
        self.assertEqual('{}'.format(self.role.party), '{}'.format(self.role.individual))
        self.role.organisation = self.organisation
        self.assertEqual('{}'.format(self.role.party), '{}'.format(self.role.organisation))
        
        with self.assertRaises(Exception):
            self.role.individual = self.organisation
        with self.assertRaises(Exception):
            self.role.organisation = self.individual

            
class PartyAdminTests(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe", form_of_address='Mr', middle_names='Hubert')
        self.organisation = Organisation.objects.create(name='Pen Inc.')
        self.phone = TelephoneNumber.objects.create(number="021123456")
        self.email = EmailContact.objects.create(email_address="test@test.com")
        self.role = GenericPartyRole.objects.create(party=self.organisation, name="Generic")
                
        self.site = AdminSite()
    
    
    def assertIsValid(self, model_admin, model):
        admin_obj = model_admin(model, AdminSite())
        errors = admin_obj.check()
        expected = []
        self.assertEqual(errors, expected)
        
        
    def test_genericpartyrole_fields(self):
        """
        Test the genericpartyrole fields.
        """
        ma = GenericPartyRoleAdmin(GenericPartyRole, self.site)
        
        self.assertTrue(ma.has_add_permission(request))

        self.assertEqual(list(ma.get_fields(request)), ['valid_to', 'name', 'party'])
        self.assertEqual(list(ma.get_form(request).base_fields), ['valid_to', 'name', 'party'])
        self.assertIsValid(GenericPartyRoleAdmin, GenericPartyRole)
       

    def test_genericpartyrole_form(self):
        """
        Test the genericpartyrole admin form .
        """
        ma = GenericPartyRoleAdmin(GenericPartyRole, self.site)
                
        mf = GenericPartyRoleAdminForm(instance=self.role)
        self.assertEqual(mf.base_fields['party'].choices[1], ('1::Individual::Mr John Hubert Doe', 'Mr John Hubert Doe'))
        
        mf.cleaned_data = {'party':"1::Individual::Mr John Hubert Doe,Mr John Hubert Doe",}
        ma.save_model('',self.role,mf,False)
        self.assertEqual(self.role.party,self.individual)
        
        mf.cleaned_data = {'party':"1::Organisation::Pen Inc.,Pen Inc.",}
        ma.save_model('',self.role,mf,False)
        self.assertEqual(self.role.party,self.organisation)

        
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
        
        