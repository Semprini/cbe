from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountContact
from cbe.party.models import Individual, Organisation, TelephoneNumber, GenericPartyRole, PartyRoleAssociation
from cbe.party.serializers import PartyRelatedField, IndividualSerializer, OrganisationSerializer, TelephoneNumberSerializer, PartyRoleAssociationFromBasicSerializer, PartyRoleAssociationToBasicSerializer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    #party = GenericRelatedField( many=False, serializer_dict={
    #        Individual: IndividualSerializer(),
    #        Organisation: OrganisationSerializer(),
    #    })
    party = PartyRelatedField()
    type = TypeField()

    associations_from = GenericRelatedField( many=True, serializer_dict={PartyRoleAssociation: PartyRoleAssociationFromBasicSerializer(), } )
    associations_to = GenericRelatedField( many=True, serializer_dict={ PartyRoleAssociation: PartyRoleAssociationToBasicSerializer(), } )
    
    class Meta:
        model = Customer
        fields = ('type', 'url', 'customer_number', 'managed_by',
                  'customer_status', 'party', 'customeraccount_set', 'associations_from', 'associations_to',)

    def create(self, validated_data):
        validated_data.pop('customeraccount_set')
        print( validated_data )
        return Customer.objects.create(**validated_data)



class CustomerAccountContactSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = GenericRelatedField( many=False,
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })

    class Meta:
        model = CustomerAccountContact
        fields = ('type', 'url', 'party', 'customeraccount_set')


class CustomerAccountSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = CustomerAccount
        fields = ('type', 'url', 'created', 'valid_from', 'valid_to', 'customer', 'account_number', 'account_status', 'managed_by', 'liability_ownership',
                  'account_type', 'name', 'pin', 'customer_account_contact', 'credit_limit', 'credit_status', 'credit_balance',)


sample_json = """
{
    "type": "Customer",
    "customer_number": "512332",
    "customer_status": "Active",
    "party": {
        "type": "Organisation",
        "name": "A cool store4"
    }
}
{
    "type": "Customer",
    "customer_number": "1512332212",
    "customer_status": "Active",
    "party": {
        "type": "Organisation",
        "url": "http://127.0.0.1:8000/api/sid/common_business_entities/party/organisations/2/"
    }
}

{ "type": "Customer","customer_number": "512332","customer_status": "Active","party": { "url":"http://127.0.0.1:8000/api/sid/organisations/2/" } }


"""
