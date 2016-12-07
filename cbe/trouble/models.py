from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from gm2m import GM2MField

from cbe.business_interaction.models import BusinessInteraction, BusinessInteractionItem

TROUBLE_TICKET_CHOICES = (('Queued','Queued'),('Active','Active'),('Deferred','Deferred'),('Cleared','Cleared'),('Closed','Closed'),('Disabled','Disabled'))

class TroubleTicket(BusinessInteraction):
    trouble_ticket_state = models.CharField(max_length=50, choices=TROUBLE_TICKET_CHOICES)
    trouble_detection_date = models.DateTimeField(default=timezone.now)
    serviceRestoredDate = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return "%s:%s at %s"%(self.trouble_ticket_state, self.description, self.trouble_detection_date)

        
class TroubleTicketItem(BusinessInteractionItem):
    trouble_ticket = models.ForeignKey(TroubleTicket)#, related_name="item_trouble_ticket")

    def __str__(self):
        return "%s:%s"%(self.trouble_ticket, self.action)
    

class Problem(models.Model):
    underlying_problems = models.ManyToManyField('Problem', blank=True)
    
    affected_locations = GM2MField()
    
    associated_trouble_tickets = models.ManyToManyField(TroubleTicket, blank=True)

    originating_system = models.CharField(max_length=100)
    # impactImportanceFactor
    # priority
    description = models.TextField()
    # firstAlert
    # category
    # responsibleParty
    # problemEscalation
    # comments
    time_raised = models.DateTimeField( auto_now_add=True )
    time_changed = models.DateTimeField( auto_now=True )
    reason = models.CharField(max_length=200)
    # ackStatus
    # clearStatus
    # activityStatus
    # impactPattterns

    def __str__(self):
        return "{}:{} at {}".format(self.originating_system, self.reason, self.time_raised)
    
    
class ResourceAlarm(models.Model):
    alarmType = models.CharField(max_length=100)
    perceivedSeverity = models.CharField(max_length=100, blank=True, null=True)
    probableCause = models.CharField(max_length=100, blank=True, null=True)
    specificProblem = models.ForeignKey(Problem, blank=True, null=True)
    # managedObjectClass
    # alarmRaisedTime
    # alarmClearedTime
    # proposedRepairActions
    additionalText = models.TextField(blank=True, null=True)
    alarmReportingTime = models.DateTimeField( auto_now_add=True )
    alarmChangedTime = models.DateTimeField( auto_now=True )
    # systemDN
    # ackState
    # ackTime
    # ackUserId
    # ackSystemId
    # clearUserId
    # clearSystemId
    # backedUpStatus

    def __str__(self):
        return "{}:{}".format(self.id, self.alarmType)

    
class TrackingRecord(models.Model):
    problem = models.ForeignKey(Problem)
    description = models.TextField(blank=True, null=True)
    system = models.CharField(max_length=100)
    time = models.DateTimeField( auto_now_add=True )
    # user
    resource_alarm = models.ForeignKey(ResourceAlarm, blank=True, null=True)
    
    def __str__(self):
        return "{}:{}:{}:{}".format(self.id, self.problem, self.system, self.time)
        