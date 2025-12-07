from rest_framework import serializers
from app.models.plannedEvent import PlannedEvent

class PlannedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedEvent
        fields = '__all__'

    
    