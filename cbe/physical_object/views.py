from rest_framework import permissions, renderers, viewsets
from cbe.physical_object.models import Structure, Vehicle

from cbe.physical_object.serializers import StructureSerializer, VehicleSerializer


class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    