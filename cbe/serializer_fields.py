from django.utils import six, timezone
from rest_framework import serializers
#from cbe.location.models import 


class PlaceRelatedField(serializers.RelatedField):
    """
    A custom field to use for the place generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        #if isinstance(value, Bookmark):
        #    return 'Bookmark: ' + value.url
        #elif isinstance(value, Note):
        #    return 'Note: ' + value.text
        #raise Exception('Unexpected type of tagged object')
        return '{}'.format(value)
        
        
class DisplayChoiceFieldSerializers(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(DisplayChoiceFieldSerializers, self).__init__(*args, **kwargs)
        self.choice_strings_to_values = dict([
            (six.text_type(key), key) for key, value in self.choices.items()
        ])
        
        
class TypeFieldSerializer(serializers.Field):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'serializer' arg up to the superclass - BOLLOCKS
        #self.serializer = kwargs.pop('serializer', None)
        
        kwargs['source'] = '__class__.__name__'
        kwargs['read_only'] = True
        super(TypeFieldSerializer, self).__init__(*args, **kwargs)
        
    def to_representation(self, value):
        return value
        
    def to_internal_value(self, data):
        print( "TYPEFIELD:%s"%data )
        return None
        
        
class ChoiceFieldSerializer(serializers.Field):
    def __init__(self, choices, *args, **kwargs):
        super(ChoiceFieldSerializer, self).__init__(*args, **kwargs)
        self.choices = choices
        
    def to_representation(self, value):
        return "%s"%self.choices[value][1]
        
    def to_internal_value(self, data):
        for choice in self.choices:
            if choice[1] == data:
                return choice[0]
        return None        