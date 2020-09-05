from django.contrib import admin

from cbe.party.admin import GenericPartyRoleAdmin

from cbe.human_resources.models import Staff, IdentificationType, Identification, Timesheet, TimesheetEntry

admin.site.register(IdentificationType)
admin.site.register(Identification)
admin.site.register(Staff,GenericPartyRoleAdmin)
admin.site.register(Timesheet)
admin.site.register(TimesheetEntry)
