"""cbe ar URL Configuration

"""
from django.conf.urls import include, url

from drf_nest.routers import AppRouter
from . import views

router = AppRouter(root_view_name='app-information_technology')
router.register(r'component', views.ComponentViewSet)
router.register(r'component', views.ComponentViewSet)
router.register(r'component_classification', views.ComponentClassificationViewSet)
router.register(r'process_framework', views.ProcessFrameworkViewSet)
router.register(r'process', views.ProcessViewSet)
router.register(r'process_classification', views.ProcessClassificationViewSet)

urlpatterns = [
    url(r'^api/information_technology/', include(router.urls)),
]

