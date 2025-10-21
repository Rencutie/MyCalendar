from django.db import models
from django.contrib.auth.models import User

class BaseScheduleEvent(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, related_name="planned_events" , on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    duration = models.DurationField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class PlannedEvent(BaseScheduleEvent):
    start_time = models.TimeField()
    recurenceRule = models.ForeignKey('RecurrenceRule', on_delete=models.CASCADE, blank=True, null=True)
    
    @property
    def end_time(self):
        if self.duration:
            from datetime import datetime
            return (datetime.combine(self.date, self.start_time) + self.duration).time()
        return None

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"