from rest_framework import serializers

from drf_nest.serializer_fields import TypeField
from cbe.location.models import GeographicArea, UrbanPropertyAddress, UrbanPropertySubAddress, RuralPropertyAddress, PoBoxAddress, Location, Country, City, Location


class GeographicAreaSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = GeographicArea
        fields = ('type', 'url', 'name')
        
        
class CitySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = City
        fields = ('type', 'url', 'code', 'name', 'country')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Country
        fields = ('type', 'url', 'code', 'name')


class UrbanPropertyAddressSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = UrbanPropertyAddress
        fields = ('type', 'url', 'country', 'city', 'province', 'locality', 'postcode', 'street_name', 'street_number_first',
                  'street_number_first_suffix', 'street_number_last', 'street_number_last_suffix', 'street_suffix', 'street_type')


class PoBoxAddressSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PoBoxAddress
        fields = ('type', 'url', 'country', 'city',
                  'province', 'locality', 'box_number',)


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = Location
        fields = ('type', 'url', 'name', 'type','postcode', 'address_line1', 'address_line2', 'latitude', 'longitude', 'rural_property_address', 'urban_property_address' )
        