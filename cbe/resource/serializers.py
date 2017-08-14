from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField

from cbe.physical_object.models import Device
from cbe.physical_object.serializers import DeviceSerializer

from cbe.resource.models import PhysicalResource

class PhysicalResourceSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    physical_objects = GenericRelatedField( many=True, serializer_dict={Device: DeviceSerializer(), } )
    
    class Meta:
        model = PhysicalResource
        fields = ('type', 'url', 'usage_state', 'name','owner','serial_number','power_state','physical_objects',)



  