from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import authantification as auth_views
from .views import PlannedEventViewSet

router = DefaultRouter()
router.register(r'events', PlannedEventViewSet, basename='plannedevent')

urlpatterns = [

    path('', include(router.urls)),
    
    path('auth/register/', auth_views.register, name='register'),
]