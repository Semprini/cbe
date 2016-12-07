from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cbe.serializer_fields import GenericRelatedField
from cbe.serializers import GenericHyperlinkedSerializer

from cbe.trouble.models import Problem
from cbe.location.models import UrbanPropertyAddress, PoBoxAddress
from cbe.location.serializers import CountrySerializer, UrbanPropertyAddressSerializer, PoBoxAddressSerializer



        
class ProblemSerializer(GenericHyperlinkedSerializer):
    underlying_problems = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='problem-detail')
    affected_locations = GenericRelatedField(many=True, serializer_dict={UrbanPropertyAddress:UrbanPropertyAddressSerializer(),PoBoxAddress:PoBoxAddressSerializer(),})

    
    class Meta:
        model = Problem
        fields = ('type', 'url', 'underlying_problems','originating_system','description','time_raised','time_changed','reason','affected_locations' )
          