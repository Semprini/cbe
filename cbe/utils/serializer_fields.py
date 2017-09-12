from urllib.parse import urlparse
from django.core.urlresolvers import resolve
from django.utils import six
from rest_framework import serializers

class ExtendedModelSerializerField(serializers.Field):
    """
    A custom field which allows urls to be provided when deserializing hyperlinked fields.
    """

    def __init__(self, serializer, many=False, *args, **kwargs):
        self.many = many
        super(ExtendedModelSerializerField, self).__init__(*args, **kwargs)

        self.serializer = serializer
        self.serializer.bind('', self)

    def to_representation(self, instance):
        # Serialize using supplied serializer
        self.serializer.expansion_depth = getattr(self, "expansion_depth", 0)
        return self.serializer.to_representation(instance)

    def to_internal_value(self, data):
        # Allow string, list or full object to be provided
        
        # If string then it must contain the URL, reverse and get referenced object
        if type(data) == str:
            resolved_func, unused_args, resolved_kwargs = resolve(
                urlparse(data).path)
            return resolved_func.cls.queryset.get(pk=resolved_kwargs['pk'])

        # If list then loop through results and call to_internal_value on each
        elif type(data) == list:
            if self.parent.instance == None:
                return []
            else:
                attr = getattr( self.parent.instance, self.source )
                setattr( self.parent.instance, self.source, [] )
                for object in data:
                    attr.add( self.to_internal_value( object ) )
                self.parent.instance.save()
                return attr.all()
        
        # Otherwise use default serializer function
        else:
            obj_internal_value = self.serializer.to_internal_value(data)
            if self.parent.instance == None:
                print( obj_internal_value )
                return obj_internal_value
            object = getattr( self.parent.instance, self.source )
            for k, v in obj_internal_value.items():
                setattr(object, k, v)
            object.save()
            return object
        
    
class GenericRelatedField(serializers.Field):
    """
    A custom field to use for serializing generic relationships.
    """

    def __init__(self, serializer_dict, *args, **kwargs):
        self.many = kwargs.pop('many')
        super(GenericRelatedField, self).__init__(*args, **kwargs)

        self.serializer_dict = serializer_dict
        for s in self.serializer_dict.values():
            s.bind('', self)


    def to_representation(self, instance):
        if self.many:
            objects = []
            for object in instance.all():
                self.to_representation(object)
            return objects

        # find a serializer correspoding to the instance class
        for key in self.serializer_dict.keys():
            if isinstance(instance, key):
                # Return the result of the classes serializer
                return self.serializer_dict[key].to_representation(instance=instance)

        return '{}'.format(instance)


    def to_internal_value(self, data):
        # If provided as string, must be url to resource. Create dict containing just url
        if type(data) == str:
            data = {'url': data}

        # If provided as list then loop through all objects
        elif type(data) == list:
            if self.parent.instance == None:
                return []
            else:
                attr = getattr( self.parent.instance, self.source )
                setattr( self.parent.instance, self.source, [] )
                for object in data:
                    attr.add( self.to_internal_value( object ) )
                self.parent.instance.save()
                return attr.all()

        # Existing resource can be specified as url
        if 'url' in data:
            # Extract details from the url and grab real object
            resolved_func, unused_args, resolved_kwargs = resolve(
                urlparse(data['url']).path)
            object = resolved_func.cls.queryset.get(pk=resolved_kwargs['pk'])
        else:
            # If url is not specified then object is new and must have a 'type'
            # field to allow us to create correct object from list of
            # serializers
            for key in self.serializer_dict.keys():
                if data['type'] == key.__name__:
                    object = key()

        # Deserialize data into attributes of object and apply
        if object.__class__ in self.serializer_dict.keys():
            serializer = self.serializer_dict[object.__class__]
            serializer.partial = True
            obj_internal_value = serializer.to_internal_value(data)
            for k, v in obj_internal_value.items():
                setattr(object, k, v)
        else:
            raise NameError(
                "No serializer specified for {} entities".format(object.__class__.__name__))

        # Save object to store new or any updated attributes
        object.save()
        return object


class TypeField(serializers.Field):
    """
        Read only Field which displays the object type from the class name
    """

    def __init__(self, *args, **kwargs):

        kwargs['source'] = '__class__.__name__'
        kwargs['read_only'] = True
        super(TypeField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        return value
