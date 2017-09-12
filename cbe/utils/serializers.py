from urllib.parse import urlparse
from collections import OrderedDict
import inspect

from django.core.urlresolvers import resolve
from django.conf import settings

from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from cbe.utils.serializer_fields import TypeField, GenericRelatedField


class LimitDepthMixin(serializers.HyperlinkedModelSerializer):
    """
    Mixin which overloads to_representation of serializer to enforce a max depth when serializing nested relations.
    When max depth is reached the response will be the url value
    """
    
    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        self.expansion_depth = getattr(self, "expansion_depth", 0)
        
        if self.expansion_depth >= settings.DEPTH_MAX:
            for field in fields:
                print( field.field_name, type(field) )
                if field.field_name == self.url_field_name:
                    attribute = field.get_attribute(instance)
                    return field.to_representation(attribute)
                    
        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            field.expansion_depth = self.expansion_depth + 1
                
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret


class GenericHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    """
        Serializer for models with generic relations.
        Includes a type field to allow GenericRelatedFields specified in the serializer to know how to serialize correctly.
        Derived from hyperlinked serializer and the url field must be present on the serializer
    """
    type = TypeField()

    def create(self, validated_data):
        # Remove generic fields from validated data and add to separate dict
        related = {}
        for field in self._fields.keys():
            if type(self._fields[field]) == serializers.ManyRelatedField:
                if type(self._fields[field].child_relation) == GenericRelatedField:
                    related[field] = validated_data.pop(field)

        # Create instance of serializers Meta.model
        instance = self.Meta.model.objects.create(**validated_data)

        # For all related fields attach the listed objects
        for field in related.keys():
            for object in related[field]:
                attr = getattr(instance, field)
                attr.add(object)

        return instance

    def update(self, instance, validated_data):

        # Create a dict of updatable fields
        fields = {}
        generics = {}
        for field in self._fields.keys():
            # Exclude read only fields
            if not self._fields[field].read_only:
                if type(self._fields[field]) != serializers.ManyRelatedField:
                    fields[field] = self._fields[field]
                else:
                    # Exclude generics but add to separate dict
                    if type(self._fields[field].child_relation) != GenericRelatedField:
                        fields[field] = self._fields[field]
                    else:
                        generics[field] = self._fields[field]

        # Set all valid attributes of the instance to the validated data
        for field in fields.keys():
            setattr(instance, field, validated_data.get(
                field, getattr(instance, field)))

        # Add any new generic relations
        for generic_attr in generics.keys():
            attr = getattr(instance, generic_attr)
            attr_objects = list(attr.all())
            for object in validated_data.get(generic_attr, getattr(instance, generic_attr)):
                if object not in attr_objects:
                    # If the object is not in the list of existing generic
                    # relations then add it
                    attr.add(object)
                else:
                    # If the object is already related then remove it from the
                    # list so we end up with a list of missing generic
                    # relations
                    attr_objects.remove(object)

            # Remove any missing generic relations if not a partial update (PUT
            # but not PATCH)
            if not self.partial:
                for object in attr_objects:
                    attr.remove(object)

        instance.save()
        return instance
