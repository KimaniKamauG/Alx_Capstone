from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from events.models import Event, EventRegistration, Category
from users.models import User
from .serializers import EventSerializer, UserSerializer, CategorySerializer, CommentSerializer, EventFeedbackSerializer
from .permissions import IsOrganizerOrReadOnly
from rest_framework import status
from django.db import models
import django_filters


class EventFilter(django_filters.FilterSet):
    """
    Custom filter set for advanced event filtering
    """
    # Title filter with case-insensitive contains lookup
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # Location filter with case-insensitive contains lookup
    location = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date range filters
    date_from = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='lte')
    
    # Capacity filters
    has_capacity = django_filters.BooleanFilter(method='filter_has_capacity')
    
    class Meta:
        model = Event
        fields = ['title', 'location', 'date_from', 'date_to']

    def filter_has_capacity(self, queryset, name, value):
        """Filter events based on available capacity"""
        if value:
            return queryset.filter(current_capacity__lt=models.F('capacity'))
        return queryset.filter(current_capacity__gte=models.F('capacity'))
    
    
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
        # To reduce the capacity by 1 everytime a user registers for an event.
        event.capacity -= 1
       
        return Response({"detail": "Successfully registered for the event", "is_waitlisted": is_waitlisted}, status=status.HTTP_201_CREATED)
            
        
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Add a comment to an event
        """
        event = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_feedback(self, request, pk=None):
        """
        Add feedback for a past event
        """
        event = self.get_object()
        if event.date_time > timezone.now():
            return Response(
                {"detail": "Cannot add feedback for future events"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EventFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def get_feedback_summary(self, request, pk=None):
        """
        Get summary of event feedback including average rating
        """
        event = self.get_object()
        feedback = event.feedback.all()
        avg_rating = feedback.aggregate(Avg('rating'))['rating__avg']
        
        return Response({
            'average_rating': avg_rating,
            'total_feedback': feedback.count(),
            'feedback': EventFeedbackSerializer(feedback, many=True).data
        })

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
