from rest_framework import serializers

from cbe.serializer_fields import TypeFieldSerializer, DisplayChoiceFieldSerializers, PlaceRelatedField
from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem, ACTION_CHOICES

        
        
class BusinessInteractionItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeFieldSerializer()
    action = DisplayChoiceFieldSerializers(choices=ACTION_CHOICES)
        
    class Meta:
        model = BusinessInteractionItem
        fields = ('type', 'url', 'business_interaction', 'quantity', 'action', )
        
        
class BusinessInteractionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeFieldSerializer()
    #business_interaction_items = serializers.HyperlinkedRelatedField( many=True, read_only=True, view_name='business_interaction_items-detail' )
    business_interaction_items = BusinessInteractionItemSerializer(many=True, read_only=True)
    place = PlaceRelatedField(read_only=True)
    
    class Meta:
        model = BusinessInteraction
        fields = ('type', 'url', 'interaction_date', 'description', 'interaction_status', 'place', 'business_interaction_items')