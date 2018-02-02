from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.serializers import IndividualSerializer, OrganisationSerializer
from cbe.party.models import Individual, Organisation
from cbe.human_resources.models import IdentificationType, Identification, Staff, Timesheet, TimesheetEntry


class IdentificationTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    issuer = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())
    
    class Meta:
        model = IdentificationType
        fields = ('type', 'url', 'name', 'issuer', 'system' )  
                 
                  
class IdentificationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    identification_type_name = serializers.SerializerMethodField()
    
    party = GenericRelatedField( many=False, url_only=True,
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })
    party_role = GenericRelatedField( many=False, url_only=True, serializer_dict={})

    class Meta:
        model = Identification
        fields = ('type', 'url', 'identification_type', 'identification_type_name', 'valid_from', 'valid_to', 'number', 'party', 'party_role')
    
    def get_identification_type_name(self,obj):
        if obj.identification_type:
            return obj.identification_type.name
        else:
            return None

       
class StaffSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = GenericRelatedField( many=False, 
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })
    company = serializers.HyperlinkedRelatedField(view_name='organisation-detail', lookup_field='enterprise_id', queryset=Organisation.objects.all())
        
    class Meta:
        model = Staff
        fields = ('type', 'url', 'company', 'party' )

        
class TimesheetEntrySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = TimesheetEntry
        fields = ('type', 'url', 'timesheet', 'project', 'start', 'end', 'duration', 'notes' )  
        
        
class TimesheetSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = Timesheet
        fields = ('type', 'url', 'staff', 'start_date', 'end_date', 'timesheet_entries' )  
        