from django.db import models

class RecurrenceRule(models.Model):
    type = models.CharField(max_length=20, choices=[
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ])
    interval = models.IntegerField(default=1)  # ex: every 2 weeks
    count = models.IntegerField(blank=True, null=True)  # number of occurrences
    until = models.DateField(blank=True, null=True)  # end date for recurrence

    def __str__(self):
        return f"{self.type} every {self.interval} (until {self.until})" if self.until else f"{self.type} every {self.interval}"