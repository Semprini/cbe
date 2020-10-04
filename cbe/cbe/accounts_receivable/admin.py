from django.contrib import admin

from cbe.accounts_receivable.models import CustomerPayment, PaymentChannel

admin.site.register(CustomerPayment)
admin.site.register(PaymentChannel)

