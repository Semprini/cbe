from rest_framework import permissions, renderers, viewsets
from cbe.physical_object.models import Structure, Vehicle, Device

from cbe.physical_object.serializers import StructureSerializer, VehicleSerializer, DeviceSerializer


class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )    