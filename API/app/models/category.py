from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='blue')

    def meta(self):
        unique_together = ('creator', 'name')
    def __str__(self):
        return self.name