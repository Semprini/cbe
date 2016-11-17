from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cbe.serializer_fields import TypeFieldSerializer,PlaceRelatedFieldSerializer
from cbe.trouble.models import Problem
from cbe.location.serializers import CountrySerializer


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeFieldSerializer()
    underlying_problems = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='problem-detail')
    affected_locations = PlaceRelatedFieldSerializer(many=True)

    class Meta:
        model = Problem
        fields = ('type', 'url', 'underlying_problems','originatingSytem','description','timeRaised','timeChanged','reason', 'affected_locations',)
     
        