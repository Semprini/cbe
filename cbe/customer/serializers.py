from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.customer.models import Customer, CustomerAccount, CustomerAccountContact
from cbe.party.models import Individual, Organisation, TelephoneNumber
from cbe.party.serializers import IndividualSerializer, OrganisationSerializer, TelephoneNumberSerializer

class PartyRelatedField(serializers.Field):

    """
    A custom field to use for the party generic relationship.
    """

    def __init__(self, *args, **kwargs):
        super(PartyRelatedField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Serialize party instances using a individual or organization serializer,
        """
        if isinstance(value, Individual):
            serializer = IndividualSerializer(value, context=self.context)
        elif isinstance(value, Organisation):
            serializer = OrganisationSerializer(value, context=self.context)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data

    def to_internal_value(self, data):
        args = {}

        # Validate args - just exlude url and type at this stage
        for key, value in data.items():
            if key != "url" and key != "type":
                args[key] = value

        if "url" in data:
            # Existing resouce
            resolved_func, unused_args, resolved_kwargs = resolve(
                urlparse(data['url']).path)
            party = resolved_func.cls.serializer_class.Meta.model.objects.get(
                pk=resolved_kwargs['pk'])
            for key, value in args.items():
                setattr(party, key, value)
        else:
            # New resource
            # TODO: some way of specifying which type of party
            if data["type"] == "Individual":
                party = Individual(**args)
            elif data["type"] == "Organisation":
                party = Organisation(**args)
            else:
                raise Exception

        party.save()
        return party


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    #party = GenericRelatedField( many=False, serializer_dict={
    #        Individual: IndividualSerializer(),
    #        Organisation: OrganisationSerializer(),
    #    })
    party = PartyRelatedField()
    type = TypeField()

    class Meta:
        model = Customer
        fields = ('type', 'url', 'customer_number',
                  'customer_status', 'party', 'customeraccount_set')

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
        fields = ('type', 'url', 'customer', 'account_number', 'account_status',
                  'account_type', 'name', 'pin', 'credit_limit', 'customer_account_contact',)


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
