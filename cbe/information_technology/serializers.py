from rest_framework import serializers

from cbe.information_technology.models import Component, ComponentClassification, Process, ProcessClassification, ProcessFramework


class ProcessFrameworkSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ProcessFramework
        fields = ('url', 'name', 'processes')
        

class ComponentClassificationSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ComponentClassification
        fields = ('url', 'name', 'documentation')


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Component
        fields = ('url', 'name', 'processes', 'classification', 'documentation', )

        
class ProcessClassificationSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ProcessClassification
        fields = ('url', 'name', 'documentation')

        
class ProcessSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Process
        fields = ('url', 'framework', 'id', 'hierarchy_id', 'level', 'parent','name','friendly_name','child_processes','components','classification','documentation', )
        