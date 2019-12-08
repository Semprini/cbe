"""cbe hr URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-customer')
router.register(r'customer', views.CustomerViewSet, base_name='customer')
router.register(r'account', views.CustomerAccountViewSet)
router.register(r'customer_account_contact', views.CustomerAccountContactViewSet)

urlpatterns = [
    url(r'^api/customer/', include(router.urls)),
]

