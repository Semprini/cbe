from rest_framework import serializers

from cbe.serializer_fields import TypeField, DisplayChoiceField, GenericRelatedField
from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem, ACTION_CHOICES

        
        
class BusinessInteractionItemSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    action = DisplayChoiceField(choices=ACTION_CHOICES)
        
    class Meta:
        model = BusinessInteractionItem
        fields = ('type', 'url', 'business_interaction', 'quantity', 'action', )
        
        
class BusinessInteractionSerializer(serializers.HyperlinkedModelSerializer):
    type = TypeField()
    #business_interaction_items = serializers.HyperlinkedRelatedField( many=True, read_only=True, view_name='business_interaction_items-detail' )
    business_interaction_items = BusinessInteractionItemSerializer(many=True, read_only=True)
    place = GenericRelatedField(read_only=True, serializer_dict={})
    
    class Meta:
        model = BusinessInteraction
        fields = ('type', 'url', 'interaction_date', 'description', 'interaction_status', 'place', 'business_interaction_items')