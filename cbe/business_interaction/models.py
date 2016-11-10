from functools import partial

from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_init, post_save

ACTION_CHOICES=(('add','add'),('update','update'),('delete','delete'))

class BusinessInteraction(models.Model):
    interaction_date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=500, null=True, blank=True)
    interaction_status = models.CharField(max_length=100, null=True, blank=True)
    previous_state = {}

    place_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_ownership") 
    place_object_id = models.PositiveIntegerField(null=True, blank=True)
    place = GenericForeignKey('place_content_type', 'place_object_id')
    
    
    def __str__(self):
        return "%s:%s at %s"%(self.interaction_date, self.description, self.place)
        
        
    @staticmethod
    def check_state(sender, **kwargs):
        instance = kwargs.get('instance')
        changes = {}
        for field in instance.previous_state.keys():
            if instance.previous_state[field] != getattr(instance, field):
                changes['{}'.format(field)] = (instance.previous_state[field], getattr(instance, field))
        return changes
                
                
    @staticmethod
    def remember_state(sender, fields, **kwargs):
        instance = kwargs.get('instance')
        for field in fields:
            instance.previous_state[field] = getattr(instance, field)

            
#NOTE FIXED DJANGO /django/dispatch/dispatcher.py line 99 & 104ish to use getfullargspec
#post_save.connect(BusinessInteraction.check_state, sender=BusinessInteraction)
#post_init.connect(partial(BusinessInteraction.remember_state, fields=('interaction_status',)), sender=BusinessInteraction, weak=False)


class BusinessInteractionItem(models.Model):
    business_interaction = models.ForeignKey(BusinessInteraction, related_name='business_interaction_items')
    quantity = models.IntegerField(null=True, blank=True)
    action = models.CharField(null=True, blank=True, max_length=50, choices=ACTION_CHOICES )

    place_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_ownership") 
    place_object_id = models.PositiveIntegerField(null=True, blank=True)
    place = GenericForeignKey('place_content_type', 'place_object_id')

    def __str__(self):
        return "%s:%s"%(self.business_interaction, self.action)    

        
class BusinessInteractionRole(models.Model):
    business_interaction = models.ForeignKey(BusinessInteraction)
    name = models.CharField(max_length=100, null=True, blank=True)

    #This can be resource or party (role?)
    interaction_role_content_type = models.ForeignKey(ContentType, null=True, blank=True, related_name="%(app_label)s_%(class)s_ownership") 
    interaction_role_object_id = models.PositiveIntegerField(null=True, blank=True)
    interaction_role = GenericForeignKey('interaction_role_content_type', 'interaction_role_object_id')

    def __str__(self):
        return "%s involved in %s as a %s"%(self.interaction_role, self.business_interaction, self.name)    
    