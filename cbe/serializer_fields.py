from urllib.parse import urlparse
from django.core.urlresolvers import resolve
from django.contrib.contenttypes.models import ContentType
from django.utils import six, timezone
from rest_framework import serializers
#from genericm2m.models import RelatedObject


class GenericRelatedField(serializers.StringRelatedField):
    """
    A custom field to use for serializing generic relationships.
    """
    def __init__(self, serializer_dict, *args, **kwargs):
        super(GenericRelatedField, self).__init__(*args, **kwargs)

        self.serializer_dict = serializer_dict
        for s in self.serializer_dict.values():
            s.bind('',self)

            
    def to_representation(self, instance):
        for key in self.serializer_dict.keys():
            if isinstance(instance, key):
                return self.serializer_dict[key].to_representation(instance=instance)
        return '{}'.format(instance)

        
    def to_internal_value(self, data):
        # If provided as string, must be url to resource. Create dict containing just url
        if type(data) == str:
            data = {'url':data}
                
        # Existing resource can be specified as url
        if 'url' in data:
            # Extract details from the url and grab real object
            resolved_func, unused_args, resolved_kwargs = resolve(urlparse(data['url']).path)
            object=resolved_func.cls.queryset.get(pk=resolved_kwargs['pk'])
        else:
            # If url is not specified then object is new and must have a 'type' field to allow us to create correct object from list of serializers
            for key in self.serializer_dict.keys():
                if data['type'] == key.__name__:
                    object = key()
        
        # Deserialize data into attributes of object and apply
        obj_internal_value = self.serializer_dict[object.__class__].to_internal_value(data)
        for k,v in obj_internal_value.items():
            setattr(object,k,v)
        
        # Save object to store new or any updated attributes
        object.save()
        return object
        
        
class DisplayChoiceField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(DisplayChoiceField, self).__init__(*args, **kwargs)
        self.choice_strings_to_values = dict([
            (six.text_type(key), key) for key, value in self.choices.items()
        ])
        
        
class TypeField(serializers.Field):
    def __init__(self, *args, **kwargs):
        
        kwargs['source'] = '__class__.__name__'
        kwargs['read_only'] = True
        super(TypeField, self).__init__(*args, **kwargs)
        
    def to_representation(self, value):
        return value
        
    #def to_internal_value(self, data):
    #    return None
        
        
       


