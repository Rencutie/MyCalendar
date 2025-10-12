from django.db import models
from django.contrib.auth.models import User
from .category import Category

class PriorityLevel(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'

class TodoItem(models.Model):
    itemId = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    priority = models.IntegerField(choices=PriorityLevel.choices, default=PriorityLevel.MEDIUM)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

 
    def __str__(self):
        return self.title
    
    