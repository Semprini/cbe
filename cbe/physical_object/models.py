from django.db import models

from cbe.party.models import Organisation, PartyRole, Owner
from cbe.location.models import Location

class PhysicalObject(models.Model):
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    physical_object_type = models.CharField(max_length=100)

    location = models.ForeignKey(Location,blank=True, null=True)
    
    class Meta:
        abstract = True

        
class ManufacturedObject(PhysicalObject):
    make = models.ForeignKey(Organisation,blank=True, null=True)
    series = models.CharField(max_length=100,blank=True, null=True)
    model = models.CharField(max_length=100,blank=True, null=True)
    serial_number = models.CharField(max_length=100,blank=True, null=True)
    owner = models.ForeignKey(Owner,blank=True, null=True)

    #TODO: Compound objects

    class Meta:
        abstract = True
        
        
class Structure(ManufacturedObject):
    name = models.CharField(max_length=200,blank=True, null=True)
    floor_square_metres = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} by {}".format(self.physical_object_type, self.make)

    def save(self, *args, **kwargs):
        if self.physical_object_type is None or self.physical_object_type == "":
            self.physical_object_type = "Structure"          
        super(Structure, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']    
        
        
class Vehicle(ManufacturedObject):
    year = models.IntegerField(blank=True, null=True)
    
    engine_capacity = models.IntegerField(blank=True, null=True)
    engine_type = models.CharField(max_length=100, blank=True, null=True)
    
    body_style = models.CharField(max_length=100, blank=True, null=True)
    doors = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    axles = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['id']    
    
    def __str__(self):
        if self.model is not None:
            return "%s %s %s" %(self.make, self.series, self.model)
        return "%s %s" %(self.make, self.series)

        
    def save(self, *args, **kwargs):
        if self.physical_object_type is None or self.physical_object_type == "":
            self.physical_object_type = "Vehicle"          
        super(Vehicle, self).save(*args, **kwargs)


class Device(ManufacturedObject):
    class Meta:
        ordering = ['id']    
    
        