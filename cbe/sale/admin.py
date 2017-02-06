from django.contrib import admin

from cbe.sale.models import Sale, SaleItem, TenderType, Tender

class TenderInline(admin.TabularInline):
    model = Tender
    extra = 0

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0


class SaleAdmin(admin.ModelAdmin):
    list_display = ('store', 'datetime','docket_number','total_amount')
    list_filter = ('datetime', 'store')
    inlines = [ TenderInline, SaleItemInline]



admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)
admin.site.register(TenderType)
admin.site.register(Tender)
