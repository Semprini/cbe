from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cbe.serializer_fields import TypeField,GenericRelatedField
from cbe.trouble.models import Problem
from cbe.location.models import UrbanPropertyAddress, PoBoxAddress
from cbe.location.serializers import CountrySerializer, UrbanPropertyAddressSerializer, PoBoxAddressSerializer


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    underlying_problems = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='problem-detail')
    affected_locations = GenericRelatedField(many=True, serializer_dict={UrbanPropertyAddress:UrbanPropertyAddressSerializer(),PoBoxAddress:PoBoxAddressSerializer(),})

    
    class Meta:
        model = Problem
        fields = ('type', 'url', 'underlying_problems','originating_system','description','time_raised','time_changed','reason', 'affected_locations',)
     
     
    def create(self, validated_data):
        al = validated_data.pop('affected_locations')
        problem = Problem.objects.create(**validated_data)
        
        for object in al:
            problem.affected_locations.connect(object)
        
        return problem

        
    def update(self, instance, validated_data):
        instance.originating_system = validated_data.get('originating_system', instance.originating_system)
        instance.description = validated_data.get('description', instance.description)
        instance.reason = validated_data.get('reason', instance.reason)
        
        #TODO: Connect any new affected locations
        
        instance.save()
        return instance        