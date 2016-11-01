from rest_framework import serializers

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