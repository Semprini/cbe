from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField
from cbe.party.serializers import PartyRelatedField
from cbe.human_resources.models import IdentificationType, Identification, Staff

                 
                  
class IdentificationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = PartyRelatedField()

    class Meta:
        model = Identification
        fields = ('type', 'url', 'identification_type', 'number', 'party')                  
        

       
class IdentificationTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = IdentificationType
        fields = ('type', 'url', 'name' )  
        
        
class StaffSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = PartyRelatedField()
    
    class Meta:
        model = Staff
        fields = ('type', 'url', 'company', 'party' )