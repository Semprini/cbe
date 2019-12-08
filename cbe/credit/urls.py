"""cbe credit URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-credit')
router.register(r'credit', views.CreditViewSet)
router.register(r'credit_alert', views.CreditAlertViewSet)
router.register(r'credit_balance_event', views.CreditBalanceEventViewSet)
router.register(r'credit_profile', views.CreditProfileViewSet)

urlpatterns = [
    url(r'^api/credit/', include(router.urls)),
]

