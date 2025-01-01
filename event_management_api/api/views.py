from .serializers import CustomUserSerializer, EventSerializer, TokenSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from events.models import Event
from rest_framework.permissions import IsAuthenticatedOrReadOnly 

User = get_user_model()

# Create your views here.
class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]





from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate 

class RegisterView(generics.GenericAPIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.GenericAPIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                token, create = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})


    
# class ProfileView(generics.GenericAPIView):
#     def get(self, request):
#         user = request.user
#         serializer = CustomUserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request):
#         user = request.user
#         serializer = CustomUserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ProfileUpdateView(generics.GenericAPIView):
#     def put(self, request, pk):
#         user_profile = UserProfile.objects.get(pk=pk)
#         serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.shortcuts import render
from rest_framework import status, generics 
from rest_framework.response import Response    
from events.models import Event, Participant  
from api.serializers import EventSerializer, ParticipantSerializer, CustomUserSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly



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