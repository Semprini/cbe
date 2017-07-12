from django.db import models

from cbe.information_technology.models import Process

class Project(models.Model):
    name = models.CharField(max_length=200)

    processes = models.ManyToManyField(Process, related_name='projects', blank=True)
    
    class Meta:
        ordering = ['id']
   
    def __str__(self):
        return self.name    
        
