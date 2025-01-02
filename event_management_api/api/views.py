# from rest_framework import viewsets, permissions, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.utils import timezone
# from .models import Event
# from .serializers import EventSerializer
# from .permissions import IsOrganizerOrReadOnly

# class EventViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for handling Event operations
    
#     Provides CRUD operations and custom actions for event management
#     """
#     serializer_class = EventSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'location', 'category']
#     ordering_fields = ['date_time', 'created_at']

#     def get_queryset(self):
#         """Return upcoming events by default"""
#         queryset = Event.objects.filter(date_time__gte=timezone.now())
        
#         # Apply date range filter if provided
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)
        
#         if start_date:
#             queryset = queryset.filter(date_time__gte=start_date)
#         if end_date:
#             queryset = queryset.filter(date_time__lte=end_date)
            
#         return queryset

#     def perform_create(self, serializer):
#         """Set the organizer to the current user when creating an event"""
#         serializer.save(organizer=self.request.user)

#     @action(detail=True, methods=['post'])
#     def register(self, request, pk=None):
#         """Handle user registration for an event"""
#         event = self.get_object()
        
#         if event.is_full:
#             return Response({"error": "Event is at capacity"}, status=400)
            
#         event.attendees.add(request.user)
#         return Response({"message": "Successfully registered for event"})

#     @action(detail=True, methods=['post'])
#     def unregister(self, request, pk=None):
#         """Handle user unregistration from an event"""
#         event = self.get_object()
#         event.attendees.remove(request.user)
#         return Response({"message": "Successfully unregistered from event"})

'''ALL THE CODE BELOW HERE WAS BEFORE ADJUSTMENTS TO THE API'''


# from .serializers import CustomUserSerializer, EventSerializer, TokenSerializer
# from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
# from django.contrib.auth import get_user_model
# from events.models import Event
# from rest_framework.permissions import IsAuthenticatedOrReadOnly 

# User = get_user_model()

# # Create your views here.
# class UserViewSet(ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CustomUserSerializer

# class EventViewSet(ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]





# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
# from django.contrib.auth import authenticate 

# class RegisterView(generics.GenericAPIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class LoginView(generics.GenericAPIView):
#     def post(self, request):
#         serializer = TokenSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(email=email, password=password)
#             if user:
#                 token, create = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key}, status=status.HTTP_200_OK)
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})


    
# # class ProfileView(generics.GenericAPIView):
# #     def get(self, request):
# #         user = request.user
# #         serializer = CustomUserSerializer(user)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
    
# #     def put(self, request):
# #         user = request.user
# #         serializer = CustomUserSerializer(user, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# # class ProfileUpdateView(generics.GenericAPIView):
# #     def put(self, request, pk):
# #         user_profile = UserProfile.objects.get(pk=pk)
# #         serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_200_OK)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# from django.shortcuts import render
# from rest_framework import status, generics 
# from rest_framework.response import Response    
# from events.models import Event, Participant  
# from api.serializers import EventSerializer, ParticipantSerializer, CustomUserSerializer
# from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticatedOrReadOnly



# # View to create an event 
# class EventCreateView(generics.CreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer

# # View to list all events with pagination 

# class EventListView(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     pagination_class = None 
#     permission_classes = [IsAuthenticatedOrReadOnly] # Allows unauthenticated read access

# # To retrieve, update and delete a single event 
# class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer

# # View to register our participant to an event

# class EventRegisterView(generics.CreateAPIView):
#     queryset = Participant.objects.all()
#     serializer_class = ParticipantSerializer

#     def perform_create(self, serializer):
#         event_id = self.kwargs['event_id']
#         event = Event.objects.get(id=event_id)
#         if event.participants_count >= event.capacity:
#             raise Exception('Event is full!')
#         serializer.save(event=event)
#         event.participants_count += 1
#         event.save()

# # View to list participants for a specific event 
# class EventParticipantsView(generics.ListAPIView):
#     serializer_class = ParticipantSerializer

#     def get_queryset(self):
#         event_id = self.kwargs['event_id']
#         return Participant.objects.filter(event__id=event_id)
    
# class UserRegisterView(generics.CreateAPIView):
#     serializer_class = CustomUserSerializer 