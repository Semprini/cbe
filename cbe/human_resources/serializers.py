from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.party.serializers import IndividualSerializer, OrganisationSerializer
from cbe.party.models import Individual, Organisation
from cbe.human_resources.models import IdentificationType, Identification, Staff, Timesheet, TimesheetEntry


class IdentificationTypeSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    class Meta:
        model = IdentificationType
        fields = ('type', 'url', 'name' )  
                 
                  
class IdentificationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    
    party = GenericRelatedField( many=False, 
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })

    class Meta:
        model = Identification
        fields = ('type', 'url', 'identification_type', 'number', 'pin', 'party', 'valid_from', 'valid_to')                  
        

       
class StaffSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    party = GenericRelatedField( many=False,
        serializer_dict={ 
            Individual: IndividualSerializer(),
            Organisation: OrganisationSerializer(),
        })
        
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
        