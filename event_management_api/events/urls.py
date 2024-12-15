from django.urls import path 
from .views import *
from rest_framework_simplejwt.views import  TokenObtainPairView


urlpatterns = [
    # These are endpoints for events and participants 
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:event_id>/register/', EventRegisterView.as_view(), name='event-register'),
    path('events/<int:event_id>/participants/', EventParticipantsView.as_view(), name='event-participants'),

    # JWT token obtain view 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # User registration endpoint 
    path('register/', UserRegisterView.as_view(), name='user-register'),
]