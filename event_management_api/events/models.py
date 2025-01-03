from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

User = get_user_model() 


# Create your models here.
class Category(models.Model):
    '''Model for event categories'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




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
    
    def available_spots(self):
        ''''Return the number of available spots for the event.'''
        return self.capacity - self.attendees.count()


class EventRegistration(models.Model):
    '''Model for managing registration and waitlist functionality
    '''
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registered_date = models.DateTimeField(auto_now_add=True)
    is_waitlisted = models.BooleanField(default=False)

    class Meta:
        unique_together = ['event', 'user'] # Prevent duplicate registrations
        ordering = ['registered_date'] # Order registrations by registration date

    def __str__(self):
        return f'{self.username} registered for {self.event.title}'