import django_filters.rest_framework
from rest_framework import filters
from rest_framework import permissions, renderers, viewsets

from cbe.human_resources.models import IdentificationType, Identification, Staff
from cbe.human_resources.serializers import IdentificationTypeSerializer, IdentificationSerializer, StaffSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.DjangoModelPermissions, )
    
    
class IdentificationViewSet(viewsets.ModelViewSet):
    queryset = Identification.objects.all()
    serializer_class = IdentificationSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    
    
    
class IdentificationTypeViewSet(viewsets.ModelViewSet):
    queryset = IdentificationType.objects.all()
    serializer_class = IdentificationTypeSerializer
    permission_classes = (permissions.DjangoModelPermissions, )    

    
