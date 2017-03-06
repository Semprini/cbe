from urllib.parse import urlparse

from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from cbe.utils.serializer_fields import TypeField, GenericRelatedField
from cbe.resource.models import PhysicalResource

class PhysicalResourceSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()

    class Meta:
        model = PhysicalResource
        fields = ('type', 'url', 'usage_state', 'name','owner','serial_number','power_state',)



  