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
from cbe.customer.admin import CustomerAccountAdmin

from requests.auth import HTTPBasicAuth

class MockRequest(object):
    pass


class MockSuperUser(object):

    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class CustomerTestCase(TestCase):

    def setUp(self):
        self.individual = Individual.objects.create(
            given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(
            party=self.individual, customer_number="1", customer_status="Open")

    def test_names(self):
        """
        Make sure the names display as expected
        """
        c1 = Customer.objects.get(customer_number=1)
        self.assertEqual(c1.customer_status, 'Open')
        self.assertEqual("{}".format(c1), '{}:{}'.format(c1.pk, c1.party))


class CustomerAccountTestCase(TestCase):

    def setUp(self):
        self.individual = Individual.objects.create(
            given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(
            party=self.individual, customer_number="1", customer_status="Open")
        self.customer_account = CustomerAccount.objects.create(
            account_number="1", account_status="Open", account_type="test", name="Test Account", customer=self.customer)

    def test_names(self):
        """
        Make sure the names display as expected
        """
        ca1 = CustomerAccount.objects.get(
            account_number=self.customer_account.account_number)
        self.assertEqual("{}".format(ca1), '{}:{}'.format(ca1.pk, ca1.name))


class CustomerAccountAdminTests(TestCase):

    def setUp(self):
        self.individual = Individual.objects.create(
            given_names="John", family_names="Doe")
        self.customer = Customer.objects.create(
            party=self.individual, customer_number="1", customer_status="Open")
        self.customer_account = CustomerAccount.objects.create(
            account_number="1", account_status="Open", account_type="test", name="Test Account", customer=self.customer)
        self.site = AdminSite()


class CustomerAccountContactTestCase(TestCase):

    def setUp(self):
        self.individual = Individual.objects.create(
            given_names="John", family_names="Doe")
        self.contact = CustomerAccountContact.objects.create(
            party=self.individual)

    def test_names(self):
        """
        Make sure the names display as expected
        """
        cac1 = CustomerAccountContact.objects.get(id=self.contact.id)
        self.assertEqual("CustomerAccountContact", '{}'.format(cac1.name))


class CustomerAPITests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.individual = Individual.objects.create(
            given_names="John", family_names="Doe")
        self.organisation = Organisation.objects.create(name='Pen Inc.')
        self.customer = Customer.objects.create(
            party=self.individual, customer_number="1", customer_status="new")
        self.factory = APIRequestFactory()

        self.client.force_authenticate(user=self.superuser)


    def test_get_customer(self):
        """
        Test that we can GET the sample Customer
        """
        view = CustomerViewSet.as_view({'get': 'list', })
        request = self.factory.get(
            '/party/customer/{}/'.format(self.customer.pk),)
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
                "url": "http://127.0.0.1:8000/api/party/individual/{}/".format(self.individual.id),
                "name": "Mr test test",
                "given_names": "test",
                "family_names": "test",
                "form_of_address": "Mr",
                "gender": "Male",
                "marital_status": "Single",
                "identifiers": []
            },
            "associations_from": [],
            "associations_to": [],
            "customer_accounts": []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(Customer.objects.get(pk='3').party.given_names, 'Bob')

        data = {
            "customer_number": "4",
            "customer_status": "new",
            "party": {
                "type": "Individual",
                "url": "http://127.0.0.1:8000/api/party/individual/{}/".format(self.individual.id),
                "name": "Mr test test",
                "given_names": "test",
                "family_names": "test",
                "form_of_address": "Mr",
                "gender": "Male",
                "marital_status": "Single",
                "identifiers": []
            },
            "associations_from": [],
            "associations_to": [],
            "customer_accounts": []
            }
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
            "associations_from": [],
            "associations_to": [],
            "party": {
                "type": "Foo"},
            "customer_accounts": []}
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
            "associations_from": [],
            "associations_to": [],
            "party": {
                "type": "Individual",
                'given_names': 'test John', 'family_names': 'Doe', 'name': 'test John Doe'},
            "customer_accounts": []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "customer_number": "4",
            "customer_status": "new",
            "associations_from": [],
            "associations_to": [],
            "party": {
                "type": "Organisation",
                'name': 'Pen Inc. 2'},
            "customer_accounts": []}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_putnpatch_customer(self):
        """
        Ensure we can update the Customer.
        """
        url = '/api/customer/customer/{}/'.format(self.customer.pk)
        data = {
            "customer_number": "3",
            "customer_status": "active",
            "associations_from": [],
            "associations_to": [],
            "party": {
                "type": "Individual",
                'given_names': 'test John', 'family_names': 'Doe', 'name': 'test John Doe'},
            "customer_accounts": []}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"customer_status": "inactive", }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
