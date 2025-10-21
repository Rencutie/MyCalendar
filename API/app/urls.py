from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import authantification as auth_views
from .views import PlannedEventViewSet

router = DefaultRouter()
router.register(r'events', PlannedEventViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', auth_views.register, name='register'),
]