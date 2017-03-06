import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.resource.models import PhysicalResource
from cbe.resource.serializers import PhysicalResourceSerializer


class PhysicalResourceViewSet(viewsets.ModelViewSet):
    queryset = PhysicalResource.objects.all()
    serializer_class = PhysicalResourceSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
