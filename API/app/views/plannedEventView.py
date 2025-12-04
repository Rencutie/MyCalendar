from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from app.models.plannedEvent import PlannedEvent
from app.Serializers import PlannedEventSerializer



class PlannedEventViewSet(viewsets.ModelViewSet):
    serializer_class = PlannedEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    

