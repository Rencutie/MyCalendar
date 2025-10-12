from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, permissions
from .models.plannedEvent import PlannedEvent
from .serializers import PlannedEventSerializer

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the Server Calendar Home Page")

class PlannedEventViewSet(viewsets.ModelViewSet):
    serializer_class = PlannedEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only events for the logged-in user
        return PlannedEvent.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        # Automatically link event to the logged-in user
        serializer.save(creator=self.request.user)
