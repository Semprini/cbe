from django.db import models
from django.utils import timezone

#from django.contrib.contenttypes.fields import GenericForeignKey
#from django.contrib.contenttypes.models import ContentType

from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem

TROUBLE_TICKET_CHOICES = (('Queued','Queued'),('Active','Active'),('Deferred','Deferred'),('Cleared','Cleared'),('Closed','Closed'),('Disabled','Disabled'))

class TroubleTicket(BusinessInteraction):
    trouble_ticket_state = models.CharField(max_length=50, choices=TROUBLE_TICKET_CHOICES)
    trouble_detection_date = models.DateTimeField(default=timezone.now)
    serviceRestoredDate = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "%s:%s at %s"%(self.trouble_ticket_state, self.description, self.trouble_detection_date)

        
class TroubleTicketItem(BusinessInteractionItem):
    def __str__(self):
        return "%s:%s"%(self.business_interaction, self.action)
    
    
# class Problem(models.Model):
    # underlying_problems = models.ManyToManyField('Problem', blank=True)
    
    # affected_locations_content_type = models.ForeignKey(ContentType, related_name="%(app_label)s_%(class)s_ownership") 
    # affected_locations_object_id = models.PositiveIntegerField()
    # affected_locations = GenericForeignKey('affected_locations_content_type', 'affected_locations_object_id', null=True, blank=True)
    
    # associated_trouble_tickets

    # originatingSytem
    # impactImportanceFactor
    # priority
    # description
    # firstAlert
    # category
    # responsibleParty
    # problemEscalation
    # comments
    # timeRaised
    # timeChanged
    # reason
    # ackStatus
    # clearStatus
    # activityStatus
    # impactPattterns
    
    
# class ResourceAlarm(models.Model):
    # alarmType
    # perceivedSeverity
    # probableCause
    # specificProblem
    # managedObjectClass
    # alarmRaisedTime
    # alarmClearedTime
    # proposedRepairActions
    # additionalText
    # alarmReportingTime
    # alarmChangedTime
    # systemDN
    # ackState
    # ackTime
    # ackUserId
    # ackSystemId
    # clearUserId
    # clearSystemId
    # backedUpStatus

    
# class TrackingRecords(models.Model):
    # problem
    # description
    # system
    # time
    # user
    # resource_alarm
    
        