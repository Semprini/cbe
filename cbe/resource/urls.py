"""cbe resource URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-resource')
router.register(r'physical_resource', views.PhysicalResourceViewSet)

urlpatterns = [
    url(r'^api/resource/', include(router.urls)),
]

