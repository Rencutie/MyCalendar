from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    planned_events = models.ManyToManyField('PlannedEvent', blank=True)
    todos = models.ManyToManyField('TodoItem', blank=True)
    owned_categories = models.ManyToManyField('Category', blank=True)