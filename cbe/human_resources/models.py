import django
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from cbe.party.models import PartyRole, Individual, Organisation
from cbe.project.models import Project

# def increment_id():
    # last = IdentificationType.objects.all().order_by('id').last()
    # if not last:
        # return 1
    # return last.id+1

class IdentificationType( models.Model ):
    name = models.CharField(max_length=200)
    issuer = models.ForeignKey(Organisation, on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)
    system = models.ForeignKey('resource.LogicalResource', on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        ret = ""
        if self.issuer:
            ret = "{}|".format(self.issuer.name)
        if self.system:
            ret += "{}|".format(self.system.name)
        return "{}{}".format(ret,self.name,)
        

class Identification( models.Model ):
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    number = models.CharField(max_length=200)
    pin = models.CharField(max_length=50, null=True, blank=True)
    identification_type = models.ForeignKey( IdentificationType, on_delete=django.db.models.deletion.CASCADE )

    party_content_type = models.ForeignKey( ContentType, on_delete=django.db.models.deletion.CASCADE, related_name="%(app_label)s_%(class)s_party_identifiers", null=True, blank=True)
    party_object_id = models.PositiveIntegerField(null=True, blank=True)
    party = GenericForeignKey('party_content_type', 'party_object_id')

    party_role_content_type = models.ForeignKey( ContentType, on_delete=django.db.models.deletion.CASCADE, related_name="%(app_label)s_%(class)s_party_role_identifiers", null=True, blank=True)
    party_role_object_id = models.PositiveIntegerField(null=True, blank=True)
    party_role = GenericForeignKey('party_role_content_type', 'party_role_object_id')
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{}:{}".format(self.identification_type, self.number,)    


class Staff(PartyRole):
    company = models.ForeignKey(Organisation, on_delete=django.db.models.deletion.CASCADE, null=True, blank=True, related_name='employer')
    identifiers = GenericRelation(Identification, object_id_field="party_object_id", content_type_field='party_content_type', related_query_name='individual')    

    def save(self, *args, **kwargs):
        if self.name is None or self.name == "":
            self.name = "Staff"
        super(Staff, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.name,)
        
        
class Timesheet(models.Model):
    staff = models.ForeignKey(Staff, on_delete=django.db.models.deletion.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    
    
class TimesheetEntry(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=django.db.models.deletion.CASCADE, related_name="timesheet_entries")
    project = models.ForeignKey(Project, on_delete=django.db.models.deletion.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    duration = models.DurationField()
    notes = models.TextField(blank=True)
    
    