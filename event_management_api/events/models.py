from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=250)
    capacity = models.PositiveIntegerField()
    participants_count = models.PositiveIntegerField(default=0)
    # To describe when the event was created or updated.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # To describe who created or updated the event.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='created_events')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, related_name='updated_events')
    
    def __str__(self):
        return self.title 
    
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField() 

    def __str__(self):
        return self.name 

