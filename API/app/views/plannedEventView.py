from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from app.models.profile import Profile
from app.models.plannedEvent import PlannedEvent
from app.Serializers import PlannedEventSerializer



class PlannedEventViewSet(viewsets.ModelViewSet):
    serializer_class = PlannedEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PlannedEvent.objects.filter(creator__user=self.request.user)

    # OVERRIDE
    def perform_create(self, serializer):
        user_profile = Profile.objects.get(user=self.request.user)
    
        serializer.save(creator=user_profile)

