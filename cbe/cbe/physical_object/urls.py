"""cbe physical_object URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-physical_object')
router.register(r'structure', views.StructureViewSet)
router.register(r'vehicle', views.VehicleViewSet)
router.register(r'device', views.DeviceViewSet)

urlpatterns = [
    url(r'^api/physical_object/', include(router.urls)),
]

