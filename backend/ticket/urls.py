from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, RequestViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 