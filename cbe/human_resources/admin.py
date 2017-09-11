from django.contrib import admin

from cbe.party.admin import GenericPartyRoleAdmin

from cbe.human_resources.models import Staff, IdentificationType, Identification

admin.site.register(IdentificationType)
admin.site.register(Identification)
admin.site.register(Staff,GenericPartyRoleAdmin)