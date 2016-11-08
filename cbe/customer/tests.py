from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.party.models import Individual, Organisation, GenericPartyRole
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountContact
from cbe.customer.views import CustomerViewSet
from cbe.customer.admin import CustomerAccountAdminForm


class CustomerTestCase(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(party=self.individual, customer_number="1", customer_status="Open")

        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        c1 = Customer.objects.get(customer_number=1)
        self.assertEqual(c1.customer_status, 'Open')
        self.assertEqual("{}".format(c1), '{}:{}'.format(c1.pk,c1.party))

        
class CustomerAccountTestCase(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(party=self.individual, customer_number="1", customer_status="Open")
        self.customer_account = CustomerAccount.objects.create(account_number="1", account_status="Open", account_type="test", name="Test Account", customer=self.customer)

        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        ca1 = CustomerAccount.objects.get(account_number=self.customer_account.account_number)
        self.assertEqual("{}".format(ca1), '{}:{}'.format(ca1.pk,ca1.name))


class CustomerAccountAdminTests(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(party=self.individual, customer_number="1", customer_status="Open")
        self.customer_account = CustomerAccount.objects.create(account_number="1", account_status="Open", account_type="test", name="Test Account", customer=self.customer)
        self.site = AdminSite()
       

    def test_customeraccountadmin_form(self):
        """
        Test the CustomerAccountAdminForm admin form .
        """
        gpr = GenericPartyRole.objects.create(party=self.individual, name="Contact")
        mf = CustomerAccountAdminForm(instance=self.customer_account)        
        self.assertFalse('contact_content_type' in list(mf.base_fields))
        self.assertEqual(mf.base_fields['customer_account_contact'].choices[1],('1::GenericPartyRole::John Doe as a Contact', 'Contact : John Doe'))
        
        
class CustomerAccountContactTestCase(TestCase):
    def setUp(self):
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.contact = CustomerAccountContact.objects.create(party=self.individual)

        
    def test_names(self):
        """
        Make sure the names display as expected
        """
        cac1 = CustomerAccountContact.objects.get(id=self.contact.id)
        self.assertEqual("CustomerAccountContact", '{}'.format(cac1.name))

        
class  CustomerAPITests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.individual = Individual.objects.create(given_names="John", family_names="Doe")
        self.organisation = Organisation.objects.create(name='Pen Inc.')
        self.customer = Customer.objects.create(party=self.individual, customer_number="1", customer_status="new")
        self.factory = APIRequestFactory()

        
    def test_get_customer(self):
        """
        Test that we can GET the sample Customer
        """
        view = CustomerViewSet.as_view({'get':'list',})
        request = self.factory.get('/party/customer/{}/'.format(self.customer.pk),)
        force_authenticate(request, user=self.superuser)
        response = view(request)
        self.assertEqual(response.exception, False)
        
    
    def test_invalid_customer_party_type(self):
        """
        Test failure if stored party generic relation is not an individual or organisation
        """
        self.customer.party_content_type = ContentType.objects.get_for_model(self.customer)
        self.customer.save()
        view = CustomerViewSet.as_view({'get':'list',})
        request = self.factory.get('/party/customer/{}/'.format(self.customer.pk),)
        force_authenticate(request, user=self.superuser)
        with self.assertRaises(Exception):
            response = view(request)
        
        
    def test_create_customer(self):
        """
        Ensure we can create a new Customer object.
        """
        url = '/api/customer/customer/'
        data = {
            "customer_number": "3",
            "customer_status": "new",
            "party": {
                "type": "Individual",
                "url": "http://127.0.0.1:8000/api/party/individual/{}/".format(self.individual.pk),
                'given_names':'Bob'},
            "customeraccount_set": [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.get(pk='3').party.given_names, 'Bob' )

        data = {
            "customer_number": "4",
            "customer_status": "new",
            "party": {
                "type": "Organisation",
                "url": "http://127.0.0.1:8000/api/party/organisation/{}/".format(self.organisation.pk)},
            "customeraccount_set": [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            
    def test_fail_create_customer_party_type(self):
        """
        Ensure incorrect party types are not accepted.
        """
        url = '/api/customer/customer/'
        data = {
            "customer_number": "3",
            "customer_status": "new",
            "party": {
                "type": "Foo"},
            "customeraccount_set": [] }
        with self.assertRaises(Exception):
            response = self.client.post(url, data, format='json')
        
        
    def test_create_customer_create_party(self):
        """
        Ensure we can create a new Customer object.
        """
        url = '/api/customer/customer/'
        data = {
            "customer_number": "3",
            "customer_status": "new",
            "party": {
                "type": "Individual",
                'given_names': 'test John', 'family_names':'Doe'},
            "customeraccount_set": [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "customer_number": "4",
            "customer_status": "new",
            "party": {
                "type": "Organisation",
                'name': 'Pen Inc. 2'},
            "customeraccount_set": [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
        
        
    def test_putnpatch_customer(self):
        """
        Ensure we can update the Individual.
        """
        url = '/api/customer/customer/{}/'.format(self.customer.pk)
        data = {
            "customer_number": "3",
            "customer_status": "active",
            "party": {
                "type": "Individual",
                'given_names': 'test John', 'family_names':'Doe'},
            "customeraccount_set": [] }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = {"customer_status": "inactive",}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        