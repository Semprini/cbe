from rest_framework import serializers

from cbe.serializer_fields import TypeFieldSerializer, DisplayChoiceFieldSerializers
from cbe.party.models import Individual, Organisation, GENDER_CHOICES, MARITAL_STATUS_CHOICES, TelephoneNumber
from cbe.location.serializers import CountrySerializer


class IndividualSerializer(serializers.HyperlinkedModelSerializer):
    #party_content_type = serializers.HyperlinkedRelatedField(view_name='contenttype-detail', queryset=ContentType.objects.filter(model__in=('organisation','individual')))
    type = TypeFieldSerializer()
    gender = DisplayChoiceFieldSerializers(choices=GENDER_CHOICES)
    marital_status = DisplayChoiceFieldSerializers(choices=MARITAL_STATUS_CHOICES)
    #nationality = CountrySerializer()    

    class Meta:
        model = Individual
        fields = ('type', 'url', 'party_user','given_names','family_names','middle_names','form_of_address', 'gender','legal_name','marital_status','nationality','place_of_birth')
        
        
class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeFieldSerializer()
    
    class Meta:
        model = Organisation
        fields = ('type', 'url', 'party_user', 'name',)   


class TelephoneNumberSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeFieldSerializer()
    
    class Meta:
        model = TelephoneNumber
        fields = ('type','url','number')
