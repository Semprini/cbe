from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from drf_nest.serializer_fields import GenericRelatedField
from drf_nest.serializers import ExtendedHyperlinkedSerialiser

from cbe.trouble.models import Problem
from cbe.location.models import UrbanPropertyAddress, PoBoxAddress, Country, City
from cbe.location.serializers import CountrySerializer, CitySerializer, UrbanPropertyAddressSerializer, PoBoxAddressSerializer


class ProblemSerializer(ExtendedHyperlinkedSerialiser):
    underlying_problems = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='problem-detail')
    affected_locations = GenericRelatedField( many=True,
        serializer_dict={
            UrbanPropertyAddress: UrbanPropertyAddressSerializer(),
            PoBoxAddress: PoBoxAddressSerializer(),
            City: CitySerializer(),
            Country: CountrySerializer(),
        }
    )

    class Meta:
        model = Problem
        fields = ('type', 'url', 'underlying_problems', 'originating_system',
                  'description', 'time_raised', 'time_changed', 'reason', 'affected_locations')
