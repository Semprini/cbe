from django.db import models

from cbe.resource.models import LogicalResource

class ProcessFramework( models.Model ):
    name = models.CharField(primary_key=True, max_length=200)

    documentation = models.TextField(blank=True)
    
    
class ProcessClassification(models.Model):
    name = models.CharField(primary_key=True, max_length=200)

    documentation = models.TextField(blank=True)

    
class Process(models.Model):
    id = models.IntegerField(primary_key=True)
    hierarchy_id = models.CharField(max_length=20)
    level = models.IntegerField(default=1)
    
    framework = models.ForeignKey(ProcessFramework, blank=True, null=True, related_name='processes')
    parent = models.ForeignKey("Process", blank=True, null=True, related_name='child_processes')
    name = models.CharField(max_length=200)
    friendly_name = models.CharField(max_length=200,blank=True, default='')

    documentation = models.TextField(blank=True)

    classification = models.ManyToManyField(ProcessClassification, blank=True)

    class Meta:
        ordering = ['id']
   
    def __str__(self):
        return "%s - %s"%(self.hierarchy_id,self.name)
        
    @property
    def get_level(self):
        l = self.hierarchy_id.count('.')
        if self.hierarchy_id[-1]!="0":
            l+=1
        return l

        
class ComponentClassification(models.Model):
    name = models.CharField(primary_key=True, max_length=200)

    documentation = models.TextField(blank=True)


class Component(models.Model):
    parent = models.ForeignKey("Component", blank=True, null=True, related_name='sub_components')

    name = models.CharField(max_length=200)
    processes = models.ManyToManyField(Process, blank=True, related_name='components')
    classification = models.ManyToManyField(ComponentClassification, blank=True)

    documentation = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

        
class Deployment(LogicalResource):
    component = models.ForeignKey(Component, related_name='deployments')

        