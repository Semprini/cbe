from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem
#from cbe.business_interaction.serializers import BusinessInteractionSerializer, BusinessInteractionItemSerializer


# class BusinessInteractionViewSet(viewsets.ModelViewSet):
    # queryset = BusinessInteraction.objects.all()
    # serializer_class = BusinessInteractionSerializer
    # permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


# class BusinessInteractionItemViewSet(viewsets.ModelViewSet):
    # queryset = BusinessInteractionItem.objects.all()
    # serializer_class = BusinessInteractionItemSerializer
    # permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
