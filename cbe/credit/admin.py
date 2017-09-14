from django.contrib import admin

from cbe.credit.models import Credit, CreditProfile, CreditAlert, CreditBalanceEvent

admin.site.register(Credit)
admin.site.register(CreditProfile)
admin.site.register(CreditAlert)
admin.site.register(CreditBalanceEvent)

