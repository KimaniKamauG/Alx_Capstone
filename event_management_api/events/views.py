from django.shortcuts import render
from rest_framework import status, generics 
from rest_framework.response import Response    
from .models import Event, Participant  
from .serializers import EventSerializer, ParticipantSerializer, CustomUserSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
# View to create an event 
class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# View to list all events with pagination 

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = None 
    permission_classes = [IsAuthenticatedOrReadOnly] # Allows unauthenticated read access

# To retrieve, update and delete a single event 
class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# View to register our participant to an event

class EventRegisterView(generics.CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def perform_create(self, serializer):
        event_id = self.kwargs['event_id']
        event = Event.objects.get(id=event_id)
        if event.participants_count >= event.capacity:
            raise Exception('Event is full!')
        serializer.save(event=event)
        event.participants_count += 1
        event.save()

# View to list participants for a specific event 
class EventParticipantsView(generics.ListAPIView):
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Participant.objects.filter(event__id=event_id)
    
class UserRegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer 