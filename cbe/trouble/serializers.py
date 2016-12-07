from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cbe.serializer_fields import TypeField,GenericRelatedField
from cbe.trouble.models import Problem
from cbe.location.models import UrbanPropertyAddress, PoBoxAddress
from cbe.location.serializers import CountrySerializer, UrbanPropertyAddressSerializer, PoBoxAddressSerializer

class GenericHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):        
        # Remove generic fields from validated data and add to separate dict
        related = {}
        for field in self._fields.keys():
            if type(self._fields[field]) == serializers.ManyRelatedField:
                if type( self._fields[field].child_relation) == GenericRelatedField:
                    related[field] = validated_data.pop(field)
                    
        # Create instance of serializers Meta.model
        instance = self.Meta.model.objects.create(**validated_data)
        
        # For all related fields attach the listed objects
        for field in related.keys():
            for object in related[field]:
                attr = getattr( instance, field )
                attr.add(object)

        return instance

        
    def update(self, instance, validated_data):
        # Create a dict of updatable fields - no read only and no generic related fields
        fields = {}
        for field in self._fields.keys():
            if not self._fields[field].read_only:
                if type(self._fields[field]) != serializers.ManyRelatedField:
                    fields[field] = self._fields[field]
                else:
                    if type( self._fields[field].child_relation) != GenericRelatedField:
                        fields[field] = self._fields[field]

        # Set all valid attributes of the instance to the validated data
        for field in fields.keys():
            setattr(instance, field, validated_data.get(field, getattr(instance,field))) 
        
        #TODO: Connect any new generics (if PUT vs PATCH)
        
        instance.save()
        return instance   

        
class ProblemSerializer(GenericHyperlinkedSerializer):
    type = TypeField()
    underlying_problems = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='problem-detail')
    affected_locations = GenericRelatedField(many=True, serializer_dict={UrbanPropertyAddress:UrbanPropertyAddressSerializer(),PoBoxAddress:PoBoxAddressSerializer(),})

    
    class Meta:
        model = Problem
        fields = ('type', 'url', 'underlying_problems','originating_system','description','time_raised','time_changed','reason','affected_locations' )
          