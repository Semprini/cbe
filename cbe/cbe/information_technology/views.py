from rest_framework import permissions, renderers, viewsets

from cbe.information_technology.models import Component, ComponentClassification, Process, ProcessClassification, ProcessFramework
from cbe.information_technology.serializers import ComponentSerializer, ComponentClassificationSerializer, ProcessSerializer, ProcessClassificationSerializer, ProcessFrameworkSerializer


class ProcessFrameworkViewSet(viewsets.ModelViewSet):
    queryset = ProcessFramework.objects.all()
    serializer_class = ProcessFrameworkSerializer

    
class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    #filter_fields = ('level',)


class ProcessClassificationViewSet(viewsets.ModelViewSet):
    queryset = ProcessClassification.objects.all()
    serializer_class = ProcessClassificationSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class ComponentClassificationViewSet(viewsets.ModelViewSet):
    queryset = ComponentClassification.objects.all()
    serializer_class = ComponentClassificationSerializer

