from rest_framework import serializers

from cbe.project.models import Project

        
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Project
        fields = ('url', 'name','processes','components',)

        
