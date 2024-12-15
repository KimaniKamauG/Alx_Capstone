from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    capacity = models.PositiveIntegerField()
    participants_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title 
    
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField() 

    def __str__(self):
        return self.name 

