from rest_framework import serializers

from drf_nest.serializer_fields import TypeField, GenericRelatedField
from cbe.party.models import GenericPartyRole, Owner, PartyRoleAssociation
from cbe.party.serializers import GenericPartyRoleSerializer
from cbe.customer.models import Customer
from cbe.customer.serializers import CustomerSerializer
   
    
class PartyRoleAssociationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    association_from = GenericRelatedField(
        many=False,
        serializer_dict={
            Customer: CustomerSerializer(),
            GenericPartyRole: GenericPartyRoleSerializer(),
        }
    )
    association_to = GenericRelatedField(
        many=False,
        serializer_dict={
            Customer: CustomerSerializer(),
            GenericPartyRole: GenericPartyRoleSerializer(),
        }
    )
    
    class Meta:
        model = PartyRoleAssociation
        fields = ('type', 'url', 'association_type','association_from','association_to')        
            