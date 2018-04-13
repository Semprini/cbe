from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from drf_nest.serializers import LimitDepthMixin
from drf_nest.serializer_fields import TypeField, ExtendedModelSerialiserField
from cbe.party.serializers import OrganisationSerializer

from cbe.party.models import Organisation
from cbe.physical_object.models import Structure, Vehicle, Device
    

class VehicleSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    make = ExtendedModelSerialiserField(OrganisationSerializer())
    
    class Meta:
        model = Vehicle
        fields = ('type', 'url', 'start_date', 'end_date', 'physical_object_type', 'make',
                  'series', 'model', 'year', 'engine_capacity', 'engine_type', 'body_style',
                  'doors','weight','axles')

                  
class StructureSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    make = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())

    class Meta:
        model = Structure
        fields = ('type', 'url', 'start_date', 'end_date', 'physical_object_type', 'name', 'floor_square_metres', 'make', 'location' )                  
        
        
class DeviceSerializer(LimitDepthMixin, serializers.HyperlinkedModelSerializer):
    type = TypeField()
    make = ExtendedModelSerialiserField(OrganisationSerializer())

    class Meta:
        model = Device
        fields = ('type', 'url', 'start_date', 'end_date', 'physical_object_type', 'make', 'location' )                          