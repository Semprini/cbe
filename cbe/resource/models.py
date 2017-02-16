from django.db import models


class Resource(models.model):
    usage_state = models.IntegerField()

    class Meta:
        abstract = True

        
class PhysicalResource(models.Model):
    power_state = models.IntegerField()
    phicial_objects = GM2MField() #TODO: Restrict to physical_object derivatives

    class Meta:
        abstract = True

        
class LogicalResource(models.Model):
    usage_state = models.IntegerField()
        
    class Meta:
            abstract = True

