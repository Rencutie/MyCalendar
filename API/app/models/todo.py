from django.db import models
from django.contrib.auth.models import User
from .category import Category
from .profile import Profile

class PriorityLevel(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'

class TodoItem(models.Model):
    itemId = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, related_name="todos",on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    priority = models.IntegerField(choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

 
    def __str__(self):
        return self.title
    
    