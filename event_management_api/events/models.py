from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model() 


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=250)
    capacity = models.PositiveIntegerField()
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)
    # To describe when the event was created or updated.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # To describe who created or updated the event.
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    
    def __str__(self):
        return self.title 
    
    def clean(self):
        '''Validate event data before saving it to the database'''
        if self.date_time < timezone.now():
            raise ValidationError('Event date cannot be in the past.')
        
    def save(self, *args, **kwargs):
        '''Override the save method to run clean before saving the event'''
        self.clean()
        super().save(*args, **kwargs)

    @property
    def is_full(self):
        ''''Check if event has reached full capacity.'''
        return self.attendees.count() >= self.capacity


    
# class Participant(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     email = models.EmailField() 

#     def __str__(self):
#         return self.name 

