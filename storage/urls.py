from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from storage.views import CollectionRequestViewSet, HistoricoAPIView, StationViewSet


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register('station', StationViewSet, basename='station')
router.register('collection-request', CollectionRequestViewSet, basename='collection-request')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/logs/<int:station_id>', HistoricoAPIView.as_view(), name='logs'),
]


