from rest_framework import serializers
from app.models.plannedEvent import PlannedEvent

class PlannedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedEvent
        fields = '__all__'

    # returns the json representation of the planned events of a given user id
    @staticmethod
    def get_planned_events_by_user_id(user_id):
        planned_events = PlannedEvent.objects.filter(user_id=user_id)
        serializer = PlannedEventSerializer(planned_events, many=True)
        return serializer.data
    