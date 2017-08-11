from urllib.parse import urlparse

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.models import Individual, Organisation, GENDER_CHOICES, MARITAL_STATUS_CHOICES, TelephoneNumber, GenericPartyRole, Owner, PartyRoleAssociation
from cbe.customer.models import Customer
from cbe.location.serializers import CountrySerializer


class PartyRelatedField(serializers.Field):

    """
    A custom field to use for party generic relationships.
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
        
        
class IndividualSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    identifications = serializers.HyperlinkedRelatedField(
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
                  'form_of_address', 'gender', 'legal_name', 'marital_status', 'nationality', 'place_of_birth', 'identifications', )


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    identifications = serializers.HyperlinkedRelatedField(
        view_name='identification-detail',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Organisation
        fields = ('type', 'url', 'parent', 'name', 'sub_organisations', 'identifications', )

        
class TelephoneNumberSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party_role = serializers.HyperlinkedRelatedField(
        view_name='genericpartyrole-detail', queryset=GenericPartyRole.objects.all())

    class Meta:
        model = TelephoneNumber
        fields = ('type', 'url', 'party_role', 'number')
        
        
class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = PartyRelatedField()
        
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
   
    