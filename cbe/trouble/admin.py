from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.contenttypes.admin import GenericTabularInline

from cbe.trouble.models import TroubleTicket, TroubleTicketItem, Problem, ResourceAlarm, TrackingRecord



class TrackingRecordInline(admin.TabularInline):
    model = TrackingRecord
    extra = 0


class TroubleTicketItemInline(admin.TabularInline):
    model = TroubleTicketItem
    fk_name = 'trouble_ticket'
    extra = 0

    
class TroubleTicketAdmin(admin.ModelAdmin):
    list_display = ('trouble_ticket_state', 'trouble_detection_date','serviceRestoredDate','description')
    inlines = [TroubleTicketItemInline,]


class TroubleTicketItemAdmin(admin.ModelAdmin):
    list_display = ('trouble_ticket', 'action','place')
    

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('originatingSytem', 'timeRaised', 'timeChanged', 'reason')


class ResourceAlarmAdmin(admin.ModelAdmin):
    list_display = ('alarmType', 'perceivedSeverity', 'probableCause', 'specificProblem','alarmReportingTime')


class TrackingRecordAdmin(admin.ModelAdmin):
    list_display = ('problem', 'system', 'time', 'resource_alarm')
    

admin.site.register(TroubleTicket, TroubleTicketAdmin)
admin.site.register(TroubleTicketItem, TroubleTicketItemAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ResourceAlarm, ResourceAlarmAdmin)
admin.site.register(TrackingRecord, TrackingRecordAdmin)
