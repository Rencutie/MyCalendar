from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    planned_events = models.ManyToManyField('plannedEvent.PlannedEvent', blank=True)
    todos = models.ManyToManyField('todo.Todo', blank=True)
    owned_categories = models.ManyToManyField('category.Category', blank=True)