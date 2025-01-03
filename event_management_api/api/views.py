from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from events.models import Event, EventRegistration, Category
from users.models import User
from .serializers import EventSerializer, UserSerializer, CategorySerializer
from .permissions import IsOrganizerOrReadOnly
from rest_framework import status

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Event operations
    
    Provides CRUD operations and custom actions for event management
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'category']
    ordering_fields = ['date_time', 'created_at']

    def get_queryset(self):
        """Return upcoming events by default"""
        queryset = Event.objects.filter(date_time__gte=timezone.now())
        
        # Apply date range filter if provided
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_time__lte=end_date)
            
        return queryset

    def perform_create(self, serializer):
        """Set the organizer to the current user when creating an event"""
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Handle user registration for an event"""
        event = self.get_object()
        user = request.user

        # Check if user is already registered for the event
        if EventRegistration.objects.filter(event=event, user=user).exists():
            return Response({"error": "User is already registered for this event"}, status=400)
        
        # Checks if the event is at full capacity 
        if event.is_full:
            return Response({"error": "Event is at maximum capacity"}, status=400)
        
        # Create registrations for the users
        current_registrations = EventRegistration.objects.filter(event=event, is_waitlisted=False).count()
        is_waitlisted = current_registrations >= event.capacity
        EventRegistration.objects.create(event=event, user=user, is_waitlisted=is_waitlisted)

        # Register the user as an attendee.
        event.attendees.add(request.user)
       
        return Response({"detail": "Successfully registered for the event", "is_waitlisted": is_waitlisted}, status=status.HTTP_201_CREATED)
            
        
        #return Response({"message": "Successfully registered for event"})

    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        """Handle user unregistration from an event"""
        event = self.get_object()
        event.attendees.remove(request.user)
        return Response({"message": "Successfully unregistered from event"})


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling User operations
    
    Provides CRUD operations for user management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """
        Override to allow user registration without authentication
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()


class CateggoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for handling Category CRUD operations
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
