from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase

from cbe.party.models import Individual
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountContact
from cbe.customer.views import CustomerViewSet


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
                "url": "http://127.0.0.1:8000/api/party/individual/{}/".format(self.individual.pk)},
            "customeraccount_set": [] }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
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
        
        