"""cbe ar URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-supplier_partner')
router.register(r'supplier', views.SupplierViewSet)
router.register(r'supplier_account', views.SupplierAccountViewSet)
router.register(r'partner', views.PartnerViewSet)
router.register(r'buyer', views.BuyerViewSet)

urlpatterns = [
    url(r'^api/supplier_partner/', include(router.urls)),
]

