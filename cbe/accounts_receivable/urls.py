"""cbe ar URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

import cbe.accounts_receivable.views as ARViews

router = AppRouter(root_view_name='app-accounts_receivable')
router.register(r'customer_payment', ARViews.CustomerPaymentViewSet)
router.register(r'payment_channel', ARViews.PaymentChannelViewSet)

urlpatterns = [
    url(r'^api/accounts_receivable/', include(router.urls)),
]

