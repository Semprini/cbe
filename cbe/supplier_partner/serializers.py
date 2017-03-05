from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.serializers import IndividualSerializer, OrganisationSerializer, TelephoneNumberSerializer
from cbe.party.serializers import PartyRelatedField
from cbe.party.models import Individual, Organisation, TelephoneNumber
from cbe.supplier_partner.models import Supplier, Buyer, Partner


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    #party = GenericRelatedField( many=False, serializer_dict={
    #        Individual: IndividualSerializer(),
    #        Organisation: OrganisationSerializer(),
    #    })
    party = PartyRelatedField()
    type = TypeField()

    class Meta:
        model = Supplier
        fields = ('type', 'url', 'party', )

    def create(self, validated_data):
        return Supplier.objects.create(**validated_data)


class PartnerSerializer(serializers.HyperlinkedModelSerializer):
    party = PartyRelatedField()
    type = TypeField()

    class Meta:
        model = Partner
        fields = ('type', 'url', 'party', )

    def create(self, validated_data):
        return Partner.objects.create(**validated_data)
 
 
class BuyerSerializer(serializers.HyperlinkedModelSerializer):
    party = PartyRelatedField()
    type = TypeField()

    class Meta:
        model = Buyer
        fields = ('type', 'url', 'party', )

    def create(self, validated_data):
        return Buyer.objects.create(**validated_data)        