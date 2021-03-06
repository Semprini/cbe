from urllib.parse import urlparse

from django.contrib.contenttypes.models import ContentType
from django.urls import resolve

from rest_framework import serializers

from drf_nest.serializers import LimitDepthMixin
from drf_nest.serializer_fields import TypeField, GenericRelatedField
from cbe.party.models import Individual, Organisation, GENDER_CHOICES, MARITAL_STATUS_CHOICES, TelephoneNumber, GenericPartyRole, Owner, PartyRoleAssociation
from cbe.customer.models import Customer
from cbe.location.serializers import CountrySerializer


class IndividualSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()

    identifiers = serializers.HyperlinkedRelatedField(
        view_name='identification-detail',
        many=True,
        read_only=True
    )
    
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES, required=False, allow_blank=True)
    marital_status = serializers.ChoiceField(
        choices=MARITAL_STATUS_CHOICES, required=False, allow_blank=True)

    class Meta:
        model = Individual
        fields = ('type', 'url', 'user', 'name', 'given_names', 'family_names', 'middle_names',
                  'form_of_address', 'gender', 'legal_name', 'marital_status', 'nationality', 'place_of_birth', 'identifiers', )

    def create(self, validated_data):
        validated_data.pop('identifiers', None)
        print(validated_data)
        return Individual.objects.create(**validated_data)
                  

class OrganisationSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    url = serializers.HyperlinkedIdentityField(
        view_name='organisation-detail',
        lookup_field='enterprise_id'
    )
    name = serializers.CharField( required=False )
    sub_organisations = serializers.HyperlinkedRelatedField(
        view_name='organisation-detail',
        many=True,
        read_only=True
    )

    identifiers = serializers.HyperlinkedRelatedField(
        view_name='identification-detail',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Organisation
        fields = ('type', 'url', 'parent', 'organisation_type', 'enterprise_id', 'name', 'sub_organisations', 'identifiers', )

        
class TelephoneNumberSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    #party_role = serializers.HyperlinkedRelatedField(
    #    view_name='genericpartyrole-detail', queryset=GenericPartyRole.objects.all())

    class Meta:
        model = TelephoneNumber
        fields = ('type', 'url', 'number')
        
        
class OwnerSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = GenericRelatedField( many=False, 
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })
        
    class Meta:
        model = Owner
        fields = ('type', 'url', 'party',)
        
        
class PartyRoleAssociationFromBasicSerializer(serializers.HyperlinkedModelSerializer):

    association_to = serializers.URLField()
    
    class Meta:
        model = PartyRoleAssociation
        fields = ( 'url', 'association_type', 'association_to' )        

        
class PartyRoleAssociationToBasicSerializer(serializers.HyperlinkedModelSerializer):

    association_from = serializers.URLField()
    
    class Meta:
        model = PartyRoleAssociation
        fields = ( 'url', 'association_type', 'association_from' )        
        
 
class GenericPartyRoleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    telephonenumbers = TelephoneNumberSerializer(many=True, read_only=True)
    
    associations_from = GenericRelatedField( many=True, serializer_dict={PartyRoleAssociation: PartyRoleAssociationFromBasicSerializer(), } )
    associations_to = GenericRelatedField( many=True, serializer_dict={ PartyRoleAssociation: PartyRoleAssociationToBasicSerializer(), } )

    class Meta:
        model = GenericPartyRole
        fields = (
            'type', 'url', 'valid_from', 'valid_to', 'name', 'telephonenumbers', 'associations_from', 'associations_to',)
   
    