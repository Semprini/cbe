from functools import partial

from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_init, post_save

ACTION_CHOICES = (('add', 'add'), ('update', 'update'), ('delete', 'delete'))

class BusinessInteraction(models.Model):
    interaction_date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=500, null=True, blank=True)
    interaction_status = models.CharField(
        max_length=100, null=True, blank=True)
    previous_state = {}

    place_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_place_ownership")
    place_object_id = models.PositiveIntegerField(null=True, blank=True)
    place = GenericForeignKey('place_content_type', 'place_object_id')

    #def __str__(self):
    #    return "%s:%s at %s" % (self.interaction_date, self.description, self.place)

    class Meta:
        abstract = True
        

class BusinessInteractionItem(models.Model):
    business_interaction_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_interaction_ownership")
    business_interaction_object_id = models.PositiveIntegerField(null=True, blank=True)
    business_interaction = GenericForeignKey('business_interaction_content_type', 'business_interaction_object_id')

    quantity = models.IntegerField(null=True, blank=True)
    action = models.CharField(
        null=True, blank=True, max_length=50, choices=ACTION_CHOICES)

    place_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_ownership")
    place_object_id = models.PositiveIntegerField(null=True, blank=True)
    place = GenericForeignKey('place_content_type', 'place_object_id')

    #def __str__(self):
    #    return "%s:%s" % (self.business_interaction, self.action)

    class Meta:
        abstract = True
        

class BusinessInteractionRole(models.Model):
    business_interaction_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_interaction_ownership")
    business_interaction_object_id = models.PositiveIntegerField(null=True, blank=True)
    business_interaction = GenericForeignKey('business_interaction_content_type', 'business_interaction_object_id')

    name = models.CharField(max_length=100, null=True, blank=True)

    # This can be resource or party (role?)
    interaction_role_content_type = models.ForeignKey(
        ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_role_ownership")
    interaction_role_object_id = models.PositiveIntegerField(
        null=True, blank=True)
    interaction_role = GenericForeignKey(
        'interaction_role_content_type', 'interaction_role_object_id')

    def __str__(self):
        return "%s involved in %s as a %s" % (self.interaction_role, self.business_interaction, self.name)
