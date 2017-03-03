from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.serializers import OrganisationSerializer
from cbe.customer.serializers import PartyRelatedField

from cbe.physical_object.models import Structure, Vehicle, Device, Owner


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = PartyRelatedField()
        
    class Meta:
        model = Owner
        fields = ('type', 'url', 'party')
    

class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    make = OrganisationSerializer()
    
    class Meta:
        model = Vehicle
        fields = ('type', 'url', 'start_date', 'end_date', 'physical_object_type', 'make',
                  'series', 'model', 'year', 'engine_capacity', 'engine_type', 'body_style',
                  'doors','weight','axles')

                  
class StructureSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Structure
        fields = ('type', 'url', 'start_date', 'end_date', 'physical_object_type', 'make' )                  
        
        
class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Structure
        fields = ('type', 'url', 'start_date', 'end_date', 'physical_object_type', 'make' )                          